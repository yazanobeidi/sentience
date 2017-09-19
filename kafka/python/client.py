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

class KafkaBase(object):
    """A high level convenience wrapper for Apache Kafka using PyKafka.

    Goals of this interface are to provide a fault-tolerant and scalable way to
    interact with the message queue.

    Use the inherited class for faster runtime at the expense of greater memory.
    """
    def __init__(self, config, log):
        """Establish connection based on config file"""
        self.zkpr = config.get('zookeeper', 'gateway')
        host = config.get('kafka', 'gateway')
        log.debug("Initializing kafka client ({})".format(host))
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
        balanced_consumer.stop()
            

    def put(self, msg, topic, pk=None):
        """Async producer."""
        topic = self.get_topic(topic)
        with topic.get_producer(linger_ms=1) as producer:
            pk = pk if pk else getrandbits(100) # any unique partition key works
            producer.produce(get_bytes(msg), partition_key=b'%i' % pk)

class Kafka(KafkaBase):
    """This class caches producer and consumer objects allowing for greater speed
    than the base class, which initializes a new producer and consumer for each
    message send / recieved.
    TODO: eventually move to its own file, for now leave here
    """
    def __init__(self, config, log, producer=None, consumer=None, **kwargs):
        log.info("Starting Kafka")
        self.log = log
        self.config = config
        self.kwargs = kwargs
        self.prod_name = None if producer is None else producer
        self.producer = None # set by user or context manager
        self.cons_name = None if consumer is None else consumer
        self.consumer = None # set by user or context manager
        self.cons_pk = 0
        self.prod_pk = 0
        KafkaBase.__init__(self, config, log)

    def __enter__(self):
        if self.prod_name: 
            self.start_producer(self.prod_name, **self.kwargs)
        if self.cons_name:
            self.start_consumer(self.cons_name, **self.kwargs)
        return self

    def __exit__(self, type, value, traceback):
        if self.producer: 
            self.stop_producer()
        if self.consumer:
            self.stop_consumer()

    def start_producer(self, producer=None, linger_ms=1, **kwargs):
        """Subscribes producer to given topic with supplied kwargs
            If producer is None will use self.producer"""
        self.log.debug("Initializing producer {}".format(producer))
        self.producer = self.get_topic(producer).get_producer(linger_ms=linger_ms,
                                                              **kwargs)
        self.producer.start()
        self.cons_pk = 0 # initialize partition key to zero

    def start_consumer(self, consumer, consumer_group=None, **kwargs):
        """Subscribes consumer to given topic and consumer group with supplied 
            kwargs
        """
        if not consumer_group:
            consumer_group = self.config.get('kafka', 'default_consumer_group')
        self.log.debug("Initializing consumer {} in consumer group <{}>".format(
                                                    consumer, consumer_group))
        self.consumer = self.get_topic(consumer)
        self.consumer = self.consumer.get_balanced_consumer(
                                    consumer_group=get_bytes(consumer_group),
                                    auto_commit_enable=True,
                                    zookeeper_connect=self.zkpr, 
                                    **kwargs)
        self.consumer.start()
        self.prod_pk = 0

    def stop_consumer(self):
        self.log.debug("stopping consumer {}".format(self.cons_name))
        self.consumer.stop()

    def stop_producer(self):
        self.log.debug("stopping producer {}".format(self.prod_name))
        self.producer.stop()
        
    def sub_producer(self, producer, **kwargs):
        """Change Producer subscription topic"""
        self.log.debug("Subscribing producer: "\
                        "{} to {}".format(self.producer, producer))
        self.producer = self.get_topic(producer).get_producer(**kwargs)
        self.prod_name = producer

    def sub_consumer(self, consumer, **kwargs):
        """Change Consumer subscription topic"""
        self.log.debug("Subscribing consumer: "\
                       "{} to {}".format(self.consumer, consumer))
        self.consumer = self.get_topic(consumer).get_consumer(**kwargs)
        self.cons_name = consumer

    def put(self, message, topic=None):
        """
        If topic is given we temporarily subscribe to that topic to post message.
        """
        #  If topic is not given use currently subscribed producer
        # and if topic does not match assigned producer, subscribe to it
        if topic is not None and topic != self.prod_name:
            self.sub_producer(topic, self.kwargs)

        #self.log.debug("kafka PUT {} -> {}".format(message, self.prod_name))

        self.producer.produce(
                        get_bytes(message), partition_key=b'%i' % self.prod_pk)

        # increment partition key
        self.prod_pk += 1

    def messages(self, meta=False, topic=None):
        """Generator object to yield continuous stream of messages.
        If meta is false, only message.value is passed.
        """
        #  If topic is not given use currently subscribed consumer
        # and if topic does not match assigned consumer, subscribe to it
        if topic is not None and topic != self.cons_name:
            self.sub_consumer(topic, self.kwargs)

        self.log.debug("kafka GET {}".format(self.cons_name))

        for message in self.consumer:
            if message is not None:
                self.log.debug("Found msg @ topic {} offset {}".format(
                                                topic, message.offset))
                # match partition key
                self.cons_pk = message.offset
                msg = message if meta else message.value
                return msg
            else:
                self.log.warning("Found None msg in topic: {}".format(topic))

    def get(self, meta=False, topic=None):
        """Return just one message from messages()"""
        return self.messages(meta=meta, topic=topic).next()


if __name__ == "__main__":
    pass