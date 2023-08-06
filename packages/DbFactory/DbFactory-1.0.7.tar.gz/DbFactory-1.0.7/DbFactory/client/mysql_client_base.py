# coding:utf-8
# author caturbhuja
# date   2020/9/7 8:50 下午 
# wechat chending2012 
# python pack
import traceback
import time

# third part pack
import pymysql
import pymysql.cursors

# self pack
from .db_base import DbBase


class MysqlClientBase(DbBase):
    def __init__(self, **kwargs):
        super(MysqlClientBase, self).__init__(**kwargs)
        self.__init_db_base_args()
        self._cursor = None
        self._conn = None
        self.__connect_init()

    def __init_db_base_args(self):
        """ 这里 填写一些默认的参数 """
        self._host = self._kwargs.pop('host', '0.0.0.0')
        self._port = int(self._kwargs.pop('port', 3306))
        self._user = self._kwargs.pop('username', 'root')
        self._passwd = self._kwargs.pop('password', 'root')
        self._db = str(self._kwargs.pop('db_name', 'siterec_dashboard'))
        self._charset = self._kwargs.pop('charset', 'utf8')
        self._autocommit = self._kwargs.pop('autocommit', False)
        self._new_kwargs = {
            "host": self._host,
            "port": self._port,
            "user": self._user,
            "passwd": self._passwd,
            "db": self._db,
            "charset": self._charset,
        }
        self._new_kwargs = {**self._kwargs, **self._new_kwargs}

    def __connect_init(self):
        i = 0
        while self._cursor is None and i < self._retry_times:
            try:
                self.reconnect()
                i += 1
                if self._conn.open:
                    self._log.info("mysql connected, host: %s, port: %d, user: %s, db: %s" % (
                        self._host, self._port, self._user, self._db))
            except Exception as e:
                self._log.error("mysql connecting error, host: %s, port: %d, user: %s, db: %s, err_msg: %s\t%s" %
                                (self._host, self._port, self._user, self._db, str(e), traceback.format_exc()))

    def __del__(self):
        self.close()

    def reconnect(self):
        try:
            self.close()
            self._conn = pymysql.connect(**self._new_kwargs)
            # self.set_character_set()  todo python2 中做法，python3 中将废弃
            self._cursor = self._conn.cursor()
            if self._conn.open:
                self._log.info("mysql reconnected, host: %s, port: %d, user: %s, db: %s" % (
                    self._host, self._port, self._user, self._db))
        except Exception as e:
            time.sleep(self._retry_sleep_time)
            self._log.error("mysql reconnecting error, host: %s, port: %d, user: %s, db: %s, err_msg: %s\t%s" %
                            (self._host, self._port, self._user, self._db, str(e), traceback.format_exc()))

    def _select_body(self, sql, mode):
        self._cursor.execute(sql)
        if mode == "many":
            ret = self._cursor.fetchall()
        else:
            ret = self._cursor.fetchone()
        return ret

    def select(self, sql, mode="many"):
        ret = None
        try:
            if self._cursor is None:
                self.reconnect()
            ret = self._select_body(sql, mode)
        except (AttributeError, pymysql.OperationalError):
            self._log.warning("mysql not connected,  host: %s, port: %d, user: %s, db: %s, sql: %s, err_msg: %s" %
                              (self._host, self._port, self._user, self._db, sql, traceback.format_exc()))
            time.sleep(self._retry_sleep_time)
            self.reconnect()
            ret = self._select_body(sql, mode)
        except Exception as e:
            self._log.error("selecting error, host: %s, port: %d, user: %s, db: %s, sql: %s, err_msg: %s\t%s" %
                            (self._host, self._port, self._user, self._db, sql, str(e), traceback.format_exc()))
            # if e.args[0] == 2006:     # todo ？
            #     self.reconnect()
        return ret

    def execute(self, sql, mode="many", args=None):
        ret_status = False
        try:
            ret_status = self._execute_body(sql, mode, args)
        except (AttributeError, pymysql.OperationalError):
            self._log.warning("mysql not connected, host: %s, port: %d, user: %s, db: %s, sql: %s, err_msg: %s" %
                              (self._host, self._port, self._user, self._db, sql, traceback.format_exc()))
            time.sleep(self._retry_sleep_time)
            ret_status = self._execute_body(sql, mode, args)
            # count = self.cursor_.execute(sql,args)
        except Exception as e:
            self.rollback()
            self._log.error("inserting error, host: %s, port: %d, user: %s, db: %s, sql: %s, err_msg: %s\t%s" %
                            (self._host, self._port, self._user, self._db, sql, str(e), traceback.format_exc()))
            # if e.args[0] == 2006:     # todo ？
            #     self.reconnect()
        return ret_status

    def _execute_body(self, sql, mode, args):
        if self._cursor is None:
            self.reconnect()
        if mode == "many":
            self._cursor.executemany(sql, args)
        else:
            self._cursor.execute(sql, args)
        self.commit()
        ret_status = True
        return ret_status

    def autocommit(self):
        self._conn.autocommit(self._autocommit)

    def set_character_set(self):
        """
        todo 这个是python2 MysqlDb 的用法。
        :return:
        """
        self._conn.set_character_set(self._charset)

    def commit(self):
        self._conn.commit()

    def rollback(self):
        self._conn.rollback()

    def close(self):
        try:
            if self._cursor is not None:
                self._cursor.close()
                self._cursor = None
            if self._conn is not None:
                self._conn.close()
                self._conn = None
        except Exception as e:
            self._log.error("mysql close error, host: %s, port: %d, user: %s, db: %s, err_msg: %s\t%s" %
                            (self._host, self._port, self._user, self._db, str(e), traceback.format_exc()))

    def get_rows_num(self):
        return self._cursor.rowcount

    @staticmethod
    def get_mysql_version():
        pymysql.get_client_info()
