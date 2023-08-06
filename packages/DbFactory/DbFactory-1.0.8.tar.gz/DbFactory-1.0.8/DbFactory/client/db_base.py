# coding:utf-8
# author caturbhuja
# date   2020/9/7 12:13 下午 
# wechat chending2012
config = dict()


class DbBase:
    def __init__(self, **kwargs):
        self._kwargs = kwargs
        self.__init_common_args()
        self.__prune_kwargs()

    def __init_common_args(self):
        global config
        config.update({
            "NO_DB_SWITCH_CLIENT": ["redis_cluster"],  # 不支持 切换db 的数据库
        })
        self._log = self._kwargs.pop('log', None)   # 这个必须有，因为 db_factory 已经处理
        self._retry_times = int(self._kwargs.pop('retry_times', 10))   # 重新连接，尝试次数
        self._retry_sleep_time = int(self._kwargs.pop('retry_sleep_time', 1))  # db 连接失败，sleep 时间

    def __prune_kwargs(self):
        """清理字典中不需要的内容，防止干扰 db 新建"""
        pop_list = ['singleton_num', 'db_type', 'singleton_sign', 'singleton_switch']
        [self._kwargs.pop(each, None) for each in pop_list]
