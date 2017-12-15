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

from kafka.python.Kafka import Kafka
from kafka.python.client import Kafka as pKafka
from src.python.utils.boilerplate import init_config_and_log

def test_kafka_base(config, log):
    with Kafka(config=config, log=log) as q:
        log.info("1. Testing ability to list topics ---------------------------")
        before = q.list_topics()
        log.info('1. SUCCESS --------------------------------------------------')
        
        log.info("2. Testing ability to make a topic---------------------------")
        topic_name = "test_topic"
        response = q.make_topic(topic_name, 1)
        log.info('make_topic() response: {}'.format(response))
        after = q.list_topics()
        log.info("before: {}\n after: {}".format(before, after))
        assert(before != after or topic_name in after)
        
        log.info('2. SUCCESS---------------------------------------------------')

        log.info("3. Testing is_topic()----------------------------------------")
        response = q.is_topic(topic_name)
        assert(response)
        log.info('is_topic() response: {}'.format(response))
        log.info('3. SUCCESS---------------------------------------------------')

        log.info("4. Testing ability to post msg-------------------------------")
        msg = "test_msg"
        q.put(msg=msg, topic=topic_name)
        response = q.get(topic_name)
        log.info('put() response: {}'.format(response))
        assert(response)
        log.info('4. SUCCESS---------------------------------------------------')

        log.info("5. Testing ability to delete topic---------------------------")
        response = q.delete_topic(topic_name)
        log.info('delete_topic() response: {}'.format(response))
        after = q.list_topics()
        assert(before == after or topic_name not in after)
        log.info('5. SUCCESS---------------------------------------------------')
    return True

def test_kafka2(config, log):
    with Kafka(config, log, producer='test_topic', consumer='test_topic') as k:
        t = time.time()
        n = 1000000
        for i in range(n):
            k.put('test_message')
        d = time.time() - t
    log.info('{} seconds, {} msg per second'.format(d, n/d))
    i = 0
    t = time.time()
    for msg in k.get():
        i += 1
    d = time.time() - t
    log.info('Retrieved {} messages in {} seconds, {} msg per second')


def speed_test(config, log):
    with Kafka(config=config, log=log) as q:
        t = time.time()
        n = 100
        # for i in range(n):
        #     q.put('test_message', 'test_topic', n)
        topic = q.get_topic('test_topic')
        with topic.get_producer(linger_ms=1) as producer:
            for i in range(n):
                producer.produce(b'test_message', partition_key=b'%i' % i)
        d = time.time() - t
    log.info('{} seconds, {} msg per second'.format(d, n/d))



if __name__ == '__main__':
    config, log = init_config_and_log(name="kafka-client")
    log.info("Starting kafka.python.client tests!!")
    if test_kafka2(config, log):
        log.info("All tests success! Kafka seems to be working.")
        log.info("Ending tests.py")
    else:
        log.error("Tests failed.")
    