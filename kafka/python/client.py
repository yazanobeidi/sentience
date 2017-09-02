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

__author__ = 'yazan'
__version__ = '0.0.1'
__licence__ = 'Apache V2'

class Kafka(object):
    """High level wrapper for Apache Kafka operations. Uses PyKafka.
    """
    def __init__(self, config, log):
        self.client = KafkaClient(hosts="127.0.0.1:9092")

    def get(self, topic=None)
        if topic:
            pass
        else:
            pass

    def put(self, topic, msg, delivery_reports=False, freq=0.001):
        with topic.get_producer(delivery_reports=delivery_reports) as producer:
            count = 0
            while True:
                count += 1
                producer.produce(msg, partition_key='{}'.format(count))
                if count % 1.0 / freq == 0:  # adjust this or bring lots of RAM ;)
                    while True:
                        try:
                            msg, exc = producer.get_delivery_report(block=False)
                            if exc is not None:
                                print 'Failed to deliver msg {}: {}'.format(
                                    msg.partition_key, repr(exc))
                            else:
                                print 'Successfully delivered msg {}'.format(
                                msg.partition_key)
                        except Queue.Empty:
                            break

    def is_topic(self, topic):
        pass

    def make_topic(self, topic, partitions):
        pass

    def rm_topic(self, topic):
        pass

    def list_topics(self):
        pass


if __name__ = "__main__":
    pass