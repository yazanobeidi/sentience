#
#                       o   o                            
#                       8                                
# .oPYo. .oPYo. odYo.  o8P o8 .oPYo. odYo. .oPYo. .oPYo. 
# Yb..   8oooo8 8' `8   8   8 8oooo8 8' `8 8    ' 8oooo8 
#   'Yb. 8.     8   8   8   8 8.     8   8 8    . 8.     
# `YooP' `Yooo' 8   8   8   8 `Yooo' 8   8 `YooP' `Yooo' 
# :.....::.....:..::..::..::..:.....:..::..:.....::.....:
# :::::::::::::::::::::::::::::::::::::::::::::::::::::::
# :::::::::::::::::::::::::::::::::::::::::::::::::::::::
#
#   Copyright Yazan Obeidi, 2017
#
#   kafka.python.client - Kafka wrapper for Python
#

from pykafka import KafkaClient
from json import dumps, loads
from uuid import uuid4

__author__ = 'yazan'
__version__ = '0.0.1'
__licence__ = 'Apache V2'

class Kafka(object):
    """A high level convenience wrapper for Apache Kafka using PyKafka.

    Goals of this interface are to provide a fault-tolerant and scalable way to
    interact with the message queue.
    """
    def __init__(self, config, log):
        """Establish connection based on config file"""
        self.zkpr = config.get('zookeeper', 'gateway')
        host = config.get('kafka', 'gateway')
        log.debug("Initializing kafka ({})".format(host))
        self.client = KafkaClient(hosts=host)
        self.config = config
        self.log = log

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        pass

    @staticmethod
    def make_request(function, _id, kwargs):
        return dumps({'function': function, 'kwargs': kwargs,'id': _id})

    def request(self, function, kwargs={}):
        """Send KafkaManager request to kafka host e.g. list topics.
        Post request to <kafka-manager-in> with randomly created ID.
        See docker-kafka/python/KafkaManager.py for more information.
        """
        # Generate the request
        _id = str(uuid4())
        request = self.make_request(function=function, _id=_id, kwargs=kwargs)
        # Post to KafkaManager input topic
        self.put(request, 'kafka-manager-in')
        # Process output
        consumer = topic.get_simple_consumer()
        for message in consumer:
            if message is not None:
                msg = loads(message.value)
                if _id == msg['id']:
                    return msg['output']

    def list_topics(self):
        """Returns list of available topics."""
        return self.request('list_topics', {})

    def is_topic(self, topic):
        """Check if topic exists"""
        return self.request('is_topic', {'topic': str(topic)})

    def make_topic(self, topic, partitions=3, replication=None):
        """Create a topic if does not exist"""
        kwargs = {'topic': topic, 
                  'partitions': partitions, 
                  'replication': replication}
        return self.request('make_topic', kwargs)

    def delete_topic(self, topic):
        """Delete single topic by name"""
        return self.request('delete_topic', {'topic': str(topic)})

    def purge_topics(self):
        """Delete all topics."""
        for topic in self.list_topics():
            if not topic.startswith(b'__'):  # leave internal topics alone
                self.delete_topic(topic)

    def get(self, 
            topic, 
            consumer_group=None, 
            continuous=False):
        """Fetches single message or optionally generates indefinite messages.
        continuous : If True function acts like a generator.
        """
        if not consumer_group:
            consumer_group = self.log.get('kafka', 'default_consumer_group')
        topic = self.client.topics[topic]
        balanced_consumer = topic.get_balanced_consumer(
                        consumer_group=consumer_group,
                        auto_commit_enable=True,
                        zookeeper_connect=':'.join([self.zk_ip, self.zk_port]))
        for message in balanced_consumer:
            if message is not None:
                self.log.debug("Found msg @ offset {}".format(message.offset))
                msg = message.value
            else:
                self.log.warning("Found None msg in topic: {}".format(topic))
            if not continuous: 
                return msg # break
            else:
                yield msg # continue to iterate

    def put(self, 
            msg, 
            topic, 
            delivery_reports=False, 
            delivery_freq=0.001):
        """Async producer with optional delivery reporting."""
        topic = self.client.topics[topic]
        with topic.get_producer(delivery_reports=delivery_reports) as producer:
            count = 0
            while True:
                count += 1
                producer.produce(msg, partition_key='{}'.format(count))
                if delivery_reports:
                    if count % (1.0 / delivery_freq) == 0:  # every 1000th one
                        while True:
                            try:
                                msg, exc = producer.get_delivery_report(block=False)
                                if exc is not None:
                                    self.log.warning(
                                        'Failed to deliver msg {}: {}'.format(
                                                msg.partition_key, repr(exc)))
                                else:
                                    self.debug(
                                            'Successfully delivered msg {}'.format(
                                                        msg.partition_key))
                            except Queue.Empty:
                                break

if __name__ == "__main__":
    pass