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
from pykafka.utils.compat import get_bytes
from json import dumps, loads
from uuid import uuid4
from random import getrandbits
import queue

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
        self.log.debug('POST {} to KafkaManager'.format(request))
        # Post to KafkaManager input topic
        self.put(request, 'kafka-manager-in')
        # Process output, simple cons. so all msgs are received by all consumers
        consumer = self.get_topic('kafka-manager-out').get_simple_consumer()
        for i, message in enumerate(consumer):
            if message is not None:
                msg = loads(message.value)
                if _id == msg['id']:
                    self.log.debug('Retrieved response: {} ({})'.format(msg, i))
                    return msg['output']

    def get_topic(self, topic):
        """Returns handle to pykafka topic instance"""
        return self.client.topics[get_bytes(topic)]

    def list_topics(self):
        """Returns list of available topics."""
        return self.request('list_topics', {})

    def is_topic(self, topic):
        """Check if topic exists"""
        return self.request('is_topic', {'topic': str(topic)})

    def make_topic(self, topic, partitions=3, replication=1):
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
            consumer_group=None):
        """Fetches single message or optionally generates indefinite messages.
        continuous : If True function acts like a generator.
        """
        if not consumer_group:
            consumer_group = self.config.get('kafka', 'default_consumer_group')
        balanced_consumer = self.get_topic(topic).get_balanced_consumer(
                        consumer_group=get_bytes(consumer_group),
                        auto_commit_enable=True,
                        zookeeper_connect=self.zkpr)
        for message in balanced_consumer:
            if message is not None:
                self.log.debug("Found msg @ offset {}".format(message.offset))
                msg = message.value
                return msg
            else:
                self.log.warning("Found None msg in topic: {}".format(topic))
            

    def put(self, msg, topic):
        """Async producer."""
        topic = self.get_topic(topic)
        with topic.get_producer() as producer:
            pk = getrandbits(100) # any unique partition key will do
            producer.produce(get_bytes(msg), partition_key=b'%i' % pk)


if __name__ == "__main__":
    pass