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

from kafka.python.client import Kafka
from src.python.utils.boilerplate import init_config_and_log

def run_tests(config, log):
    with Kafka(config=config, log=log) as q:
        log.info("Testing ability to list topics")
        before = q.list_topics()
        topic_name = "test_topic"
        log.info("Testing ability to make a topic")
        q.make_topic(topic_name, 1)
        after = q.list_topics()
        assert(before != after)
        log.info("Testing is_topic()")
        assert(q.is_topic(topic_name))
        log.info("Testing ability to post msg")
        msg = "test_msg"
        q.put(msg=msg, topic=topic_name)
        response = q.get(topic_name)
        assert(response)
        log.info("Testing ability to delete topic")
        after = q.delete_topic(topic_name)
        assert(before == after)
    return True


if __name__ == '__main__':
    config, log = init_config_and_log(name="interactor")
    log.info("Starting kafka.python.client tests!")
    if run_tests(config, log):
        log.info("All tests success! Kafka seems to be working.")
        log.info("Ending tests.py")
    else:
        log.error("Tests failed.")
    