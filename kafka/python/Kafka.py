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

from confluent_kafka import Producer, Consumer, KafkaError

from json import dumps, loads
from uuid import uuid4
from random import getrandbits
import queue

__author__ = 'yazan'
__version__ = '0.0.1'
__licence__ = 'Apache V2'


class Kafka(object):
    """A high level convenience wrapper for Apache Kafka using Confluent Kafka.

    Goals of this interface are to provide a fault-tolerant and scalable way to
    interact with the message queue.

    Use the inherited class for faster runtime at the expense of greater memory.
    """
    def __init__(self, config, log):
        """Establish connection based on config file"""
        broker = config.get('kafka', 'gateway')
        log.debug("Initializing kafka client ({})".format(broker))
        self.conf = {'bootstrap.servers': broker}
        self.producer = Producer(**conf)
        self.consumer = Consumer(**conf)
        self.config = config
        self.log = log

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        self.consumer.close()
        self.producer.close()
        pass

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

    def put(self, message, topic=None):
        """
        If topic is given we temporarily subscribe to that topic to post message.
        """
        #  If topic is not given use currently subscribed producer
        # and if topic does not match assigned producer, subscribe to it
        pass

    def messages(self, meta=False, topic=None):
        """Generator object to yield continuous stream of messages.
        If meta is false, only message.value is passed.
        """
        #  If topic is not given use currently subscribed consumer
        # and if topic does not match assigned consumer, subscribe to it
        pass

    def get(self, meta=False, topic=None):
        """Return just one message from messages()"""
        return self.messages(meta=meta, topic=topic).next()