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
    def __init__(self, config, log, group=None):
        """Establish connection based on config file"""
        if group is None:
            group = config.get('kafka','default_consumer_group')
        broker = config.get('kafka', 'gateway')
        log.debug("Initializing kafka client ({})".format(broker))
        self.prod_conf = {'bootstrap.servers': broker}
        self.cons_conf = {'bootstrap.servers': broker, 'group.id': group,
                          'default.topic.config': {'auto.offset.reset': 'beginning',
                          'enable.auto.commit': 'false'},
                          #"debug": "cgrp,protocol,topic",
                          "topic.metadata.refresh.interval.ms": 1000}
        self.producer = Producer(**self.prod_conf)
        self.consumer = Consumer(**self.cons_conf)
        self.config = config
        self.log = log
        self.cons_topics = []

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        self.consumer.close()

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
        for msg in self.stream('kafka-manager-out', meta=True, commit=False):
            self.log.debug('Retrieved response: {}'.format(msg.value()))
            msg_dict = loads(msg.value())
            if _id == msg_dict['id']:
                self.consumer.commit()
                return msg_dict['output']

    def sub(self, topic):
        if topic not in self.cons_topics:
            self.log.debug('Subscribing consumer to {}'.format(topic))
            self.cons_topics.append(topic)
            self.consumer.subscribe(self.cons_topics)

    def unsub(self):
        self.log.debug("Unassigning consumer")
        self.consumer.unassign()
        self.log.debug("Unsubscribing consumer")
        self.consumer.unsubscribe()

    def put(self, message, topic):
        """
        If topic is given we temporarily subscribe to that topic to post message.
        """
        self.producer.produce(topic, message)
        self.producer.flush()
        
    def stream(self, 
               topic, 
               persist=False, 
               meta=False, 
               timeout=3, 
               retries=15,
               commit=True):
        """Generator object to yield continuous stream of messages.
        If meta is false, only message.value is passed.
        """
        #  If topic is not given use currently subscribed consumer
        # and if topic does not match assigned consumer, subscribe to it
        self.sub(topic)
        self.log.debug('Begin polling message stream (topic: {})'.format(topic))
        end_of_offset = False
        while True:
            self.log.debug("Polling ... {}".format(
                           self.consumer.committed(
                           self.consumer.assignment())))
            msg = self.consumer.poll(timeout=timeout)
            if end_of_offset:
                if retries <= 0:
                    break
                else: 
                    retries -= 1
            if msg is None:
                continue
            if msg.error():
                if msg.error().code() == KafkaError._PARTITION_EOF:
                    # End of partition event
                    self.log.debug('%% %s [%d] reached end at offset %d' %
                                     (msg.topic(), msg.partition(), msg.offset()))
                    end_of_offset = False if persist else True
                else:
                    self.log.error("msg.error(): KafkaException")
                    raise KafkaException(msg.error())
            else:
                # Proper message
                end_of_offset = False
                self.log.debug('message %s [%d] at offset %d with key %s:' %
                                 (msg.topic(), msg.partition(), msg.offset(),
                                  str(msg.key())))
                self.log.debug('message value: {}'.format(msg.value()))
                if commit:
                    self.consumer.commit()
                yield msg if meta else msg.value()
        self.unsub()

    def get(self, topic, meta=False):
        """Return just one message from messages()"""
        msg = next(self.stream(meta=meta, topic=topic))
        self.unsub()
        return msg