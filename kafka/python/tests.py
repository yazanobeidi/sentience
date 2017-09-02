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

if __name__ == '__main__':
    print("Starting kafka.python.client tests!")
    q = Kafka()
    print("Testing ability to list topics")
    before = q.list_topics()
    topic_name = "test_topic"
    print("Testing ability to make a topic")
    q.make_topic(topic_name, 1)
    after = q.list_topics()
    assert(before != after)
    print("Testing is_topic()")
    assert(q.is_topic(topic_name))
    print("Testing ability to post msg")
    msg = "test_msg"
    q.put(msg=msg, topic=topic_name)
    response = q.get(topic_name)
    print("Testing ability to remove topic")
    after = q.rm_topic(topic_name)
    assert(before == after)
    print("All tests success! Kafka seems to be working.")
    print("Ending tests.py")
    