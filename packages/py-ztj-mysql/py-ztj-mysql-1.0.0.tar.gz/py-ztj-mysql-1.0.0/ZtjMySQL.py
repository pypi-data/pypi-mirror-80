# -*- coding: utf-8 -*-
# Intro: MySQL实例模块
# Author: Ztj
# Email: ztj1993@gmail.com
# Version: 1.0.0
# Date: 2020-09-24

import os
import time

import pymysql
from DBUtils.PooledDB import PooledDB
from pymysql.connections import Connection
from pymysql.cursors import DictCursor

__version__ = '1.0.0'


class MySQL(object):

    def __init__(self, options=None):
        self._pool = None
        self._connection = None
        self._options = options if isinstance(options, dict) else dict()

    def environment(self):
        prefix = os.environ.get('ENV_PREFIX_MYSQL', 'MYSQL')
        prefix = prefix if prefix.endswith('_') else prefix + '_'
        for key, value in os.environ.items():
            if not key.startswith(prefix):
                continue
            self._options[key[len(prefix):].lower()] = value

    def options(self):
        options = dict()
        options['host'] = self._options.get('host', '127.0.0.1')
        options['port'] = int(self._options.get('port', 3306))
        options['user'] = self._options.get('user', 'root')
        options['password'] = self._options.get('password', '')
        options['charset'] = self._options.get('charset', 'utf8')
        return options

    def pool(self) -> PooledDB:
        if self._pool is None:
            self._pool = PooledDB(creator=pymysql, cursorclass=DictCursor, **self.options())
        return self._pool

    def destroy(self):
        self._pool = None
        self._connection = None

    def reconnection(self) -> Connection:
        return self.pool().connection()

    def connection(self) -> Connection:
        if self._connection is None:
            self._connection = self.reconnection()
        return self._connection

    def ping(self) -> bool:
        try:
            self.connection().ping()
            return True
        except:
            return False

    def wait(self, interval=60, retry=100, callback=None):
        for i in range(retry):
            if self.ping():
                return True
            if callback is not None:
                callback(i, interval, self)
            time.sleep(interval)
        return False

    def exec_sql(self, sql):
        connection = self.connection()
        with connection.cursor() as cursor:
            if isinstance(sql, str):
                cursor.execute(sql)
            else:
                cursor.execute(*sql)
            connection.commit()

    def exec_sql_list(self, sql_list):
        connection = self.connection()
        with connection.cursor() as cursor:
            for sql in sql_list:
                if isinstance(sql, str):
                    cursor.execute(sql)
                else:
                    cursor.execute(*sql)
            connection.commit()

    def get_record(self, sql, callback, *args, **kwargs):
        connection = self.connection()
        with connection.cursor() as cursor:
            if isinstance(sql, str):
                cursor.execute(sql)
            else:
                cursor.execute(*sql)
            result = callback(cursor, *args, **kwargs)
        return result

    @staticmethod
    def record_callback_fetch_all(cursor: DictCursor):
        return cursor.fetchall()

    @staticmethod
    def record_callback_fetch_one(cursor: DictCursor):
        return cursor.fetchone()

    @staticmethod
    def record_callback_fetch_value(cursor: DictCursor, field=None):
        row = cursor.fetchone()
        return list(row.values())[0] if field is None else row.get(field)
