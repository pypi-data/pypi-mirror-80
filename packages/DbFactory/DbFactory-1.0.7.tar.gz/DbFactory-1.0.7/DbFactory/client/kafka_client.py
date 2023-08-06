# coding:utf-8
# author caturbhuja
# date   2020/9/7 3:06 下午 
# wechat chending2012
# python pack
import time
import multiprocessing
import signal
import traceback

# third part pack
from kafka import KafkaConsumer, TopicPartition, KafkaProducer

# self pack
from .db_base import DbBase, config


class KafkaClient(multiprocessing.Process, DbBase):
    def __init__(self, **kwargs):
        DbBase.__init__(self, **kwargs)
        self.__init_db_base_args()
        self.__init_process_args()
        # super(KafkaClient, self).__init__(name=self.__process_name, **kwargs)
        super(KafkaClient, self).__init__(name=self.__process_name)     # todo 这个版本只用到这个。暂时不处理其他参数。
        self.__init_kafka()

    def __init_db_base_args(self):
        """处理kafka基础参数"""
        self._init_type = self._kwargs.pop("init_type", 'consumer')
        self._bootstrap_servers = self._kwargs.pop("bootstrap_servers", None)
        self._group_id = self._kwargs.pop("group_id", "Haribol")
        self._topic = self._kwargs.pop("topic", None)   # todo 是否需要检查topic？
        self._partition = self._kwargs.pop("partition", None)

    def __init_process_args(self):
        self.__process_name = "{}_{}".format(self._topic, self._partition)
        '''设置信号量'''
        signal.signal(signal.SIGINT, self.__signal_handle)
        signal.signal(signal.SIGTERM, self.__signal_handle)
        self._alive = True

    def __signal_handle(self, signum, frame):
        self._log.info(self.__process_name + '\tterminate singal\t' + str(signum))
        self._alive = False

    def __init_kafka(self, count=0):
        """如果断开连接，则一直重试，直到成功"""
        try:
            if self._init_type == 'consumer':
                self.client__ = KafkaConsumer(bootstrap_servers=self._bootstrap_servers, group_id=self._group_id)
                self.client__.assign([TopicPartition(self._topic, self._partition)])
            else:
                self.client__ = KafkaProducer(bootstrap_servers=self._bootstrap_servers)
        except Exception as e:
            count += 1
            self._log.error('the {} times init_kafka error: {}\t{}'.format(count, str(e), traceback.format_exc()))
            time.sleep(self._retry_sleep_time)
            self.__init_kafka(count)

    def get_partitions_list(self, topic=None):
        """todo 这个需要考虑下如何使用？这个应该在类，实例化，之前？ 计划阅读 kafka 源码。再处理"""
        try:
            if not topic:
                topic = self._topic
            consumer = KafkaConsumer(topic, bootstrap_servers=self._bootstrap_servers)
            consumer.topics()
            partitions_list = consumer.partitions_for_topic(topic)
        except Exception as e:
            partitions_list = None
            self._log.error('get_partitions_list error: {}\t{}'.format(e, traceback.format_exc()))
        return partitions_list
