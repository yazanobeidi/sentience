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
from time import sleep

from kafka.python.client import Kafka
from src.python.utils.boilerplate import init_config_and_log

def run_tests(config, log):
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


if __name__ == '__main__':
    config, log = init_config_and_log(name="kafka-client")
    log.info("Starting kafka.python.client tests!!")
    if run_tests(config, log):
        log.info("All tests success! Kafka seems to be working.")
        log.info("Ending tests.py")
    else:
        log.error("Tests failed.")
    