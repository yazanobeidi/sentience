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

import os
import subprocess
from pykafka import KafkaClient
from shlex import quote

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
        self.ip = config.get('kafka', 'ip')
        self.port = config.get('kafka', 'port')
        self.zk_ip = config.get('zookeeper', 'ip')
        self.zk_port = config.get('zookeeper', 'port')
        host = ":".join([self.ip, self.port])
        log.debug("Initializing kafka ({})".format(host))
        self.client = KafkaClient(hosts=host)
        self.config = config
        self.log = log

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        pass

    def _run_topics_sh(self, args):
        """Run kafka-topics.sh with the provided list of arguments.
           Taken from PyKafka source code."""
        bin_dir = self.config.get('kafka', 'bin_dir')
        binfile = os.path.join(bin_dir, 'bin/kafka-topics.sh')
        zkpr = ':'.join([self.zk_ip, self.zk_port])
        cmd = [binfile, '--zookeeper', zkpr] + args
        cmd = ' '.join([str(c) for c in cmd]) # cmd needs to be str
        cmd = quote(cmd) # escape cmd for safety
        self.log.debug("running: {}".format(cmd))
        return subprocess.check_output(cmd)

    def is_topic(self, topic):
        """Check if topic exists"""
        topic in self.topics

    def get_topic(self, topic, autocreate=True, **kwargs):
        if not self.is_topic(topic):
            self.log.warning("Topic not found: {}".format(topic))
            self.make_topic(topic, **kwargs)
        return self.topics[topic]

    def make_topic(self, 
                   topic, 
                   partitions=3, 
                   replication=None):
        """Use kafka-topics.sh to create a topic."""
        log.info("Creating topic {}".format(topic_name))
        cmd = ['--create',
               '--topic', topic_name,
               '--partitions', num_partitions]
        cmd.extend(['--replication-factor', replication_factor])
        assert(len(cmd) == 8) # unexpected cmd size
        self._run_topics_sh(cmd)
        time.sleep(1)

    def delete_topic(self, topic):
        """Delete single topic by name"""
        self.log.info("Deleting topic {}".format(topic))
        self._run_topics_sh(['--delete', '--topic', topic_name])

    def list_topics(self):
        res = self._run_topics_sh(['--list'])
        return res.strip().split(b'\n')

    def purge_topics(self):
        """Delete all topics."""
        for topic in self.list_topics():
            if not topic.startswith(b'__'):  # leave internal topics alone
                self.delete_topic(topic)

    def get(self, 
            topic, 
            consumer_group=None, 
            continuous=False):
        if not consumer_group:
            consumer_group = self.log.get('kafka', 'default_consumer_group')
        balanced_consumer = topic.get_balanced_consumer(
                        consumer_group=consumer_group,
                        auto_commit_enable=True,
                        zookeeper_connect=':'.join([self.zk_ip, self.zk_port]))
        for message in balanced_consumer:
            if message is not None:
                self.log.debug("Found msg @ offset {}".format(message.offset))
                msg = message.value
            else:
                self.log.warning("Found None msg in topic: {}".format(topic))
            if not continuous: 
                return msg # break
            else:
                yield msg # continue to iterate

    def put(self, 
            msg, 
            topic, 
            delivery_reports=False, 
            delivery_freq=0.001):
        with topic.get_producer(delivery_reports=delivery_reports) as producer:
            count = 0
            while True:
                count += 1
                producer.produce(msg, partition_key='{}'.format(count))
                if delivery_reports:
                    if count % (1.0 / delivery_freq) == 0:  # every 1000th one
                        while True:
                            try:
                                msg, exc = producer.get_delivery_report(block=False)
                                if exc is not None:
                                    self.log.warning(
                                        'Failed to deliver msg {}: {}'.format(
                                                msg.partition_key, repr(exc)))
                                else:
                                    self.debug(
                                            'Successfully delivered msg {}'.format(
                                                        msg.partition_key))
                            except Queue.Empty:
                                break

if __name__ == "__main__":
    pass