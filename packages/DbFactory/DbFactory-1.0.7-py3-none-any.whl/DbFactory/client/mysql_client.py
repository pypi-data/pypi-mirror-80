#!/usr/bin/env python
# -*- coding: utf-8 -*-
# wechat: chending2012

# python pack

# third part pack

# self pack
from DbFactory.util.decorator import cost_time
from .db_base import config
# from .mysql_client_base import MysqlClientBase
from DbFactory.util.decorator import try_and_reconnect
from .mysql_client_torndb import Connection as MysqlClientBase


class MysqlClient:
    def __init__(self, **kwargs):
        self.client__ = MysqlClientBase(**kwargs)

    @cost_time(warning_time=config.get("ACTION_WARNING_TIME", 10))
    def generation_func(self, method, *args, **kwargs):
        """建立反射"""
        def action():
            return getattr(self.client__, method)(*args, **kwargs)

        return try_and_reconnect(self.client__, action)
