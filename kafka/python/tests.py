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
#   kafka.python.client - Testing methods for Kafka wrapper
#
import time

from kafka.python.kafka import Kafka
from src.python.utils.boilerplate import init_config_and_log

__author__ = 'yazan'
__version__ = '0.0.1'
__licence__ = 'Apache V2'  

def test_kafka_admin(kafka, log):
    topics = kafka.list_topics()
    log.info("{} topics found: {}".format(len(topics), topics))
    log.info("Creating test topic")
    before = kafka.list_topics()
    topic_name = "test_topic"
    response = kafka.make_topic(topic=topic_name, partitions=1)
    after = kafka.list_topics()
    log.info("Before: {}\n after: {}".format(before, after))
    assert(before != after or topic_name in after)
    log.info("Checking if test topic exists")
    assert(kafka.is_topic(topic_name))
    log.info("Deleting test topic")
    kafka.delete_topic(topic_name)
    assert(kafka.is_topic(topic_name) is False)

def test_com(kafka, log):
    topic = 'debug'
    for i in range(10):
        kafka.put('test msg {}'.format(i), topic)
        log.info("Generated {}".format(i))
    msg = kafka.get(topic)
    log.info('msg 1: {}'.format(msg))
    msg = kafka.get(topic)
    log.info('msg 2: {}'.format(msg))
    log.info('enterring stream')
    for msg in kafka.stream(topic):
        log.info("Retrieved: {}".format(msg))


if __name__ == '__main__':
    config, log = init_config_and_log(name="kafka-test")
    log.info("Initiating kafka.python.tests")
    with Kafka(config=config, log=log) as kafka:
        #test_com(kafka, log)
        test_kafka_admin(kafka, log)
    log.info("Tests complete!")