# -*- coding: utf-8 -*-

import psycopg2

from ..schema.schema import Schema, schemas


class StorageException(Exception):
    def __init__(self, info):
        super().__init__(self)
        self._info = info

    def __str__(self):
        return self._info


class Storage(object):
    _table = 'repo'

    def __init__(self, config=None):
        if config is None:
            raise StorageException('config invalid')

        self._config = config
        self._conn = None
        self._cur = None

        for item in self._config.langs:
            try:
                self._new_db(item)
                self._new_tbl(item, schemas)
            except StorageException as e:
                raise StorageException('init invalid %s' % str(e))

    def run(self, data):
        self._connect_db(data[Schema.LANGUAGE])
        self._insert_data(data)
        self._close_db()

    def _new_db(self, name):
        self._connect_db()

        try:
            self._cur.execute('create database %s;' % name)
        except psycopg2.errors.DuplicateDatabase:
            pass

        self._close_db()

    def _new_tbl(self, dbname, tblnames):
        self._connect_db(dbname)

        try:
            buf = ' text,'.join(tblnames)
            self._cur.execute('create table %s (id serial primary key, %s);' % (self._table, buf+' text'))
            self._cur.execute('alter table %s add constraint id_cons unique(%s);' % (self._table, Schema.URL))
        except psycopg2.errors.DuplicateTable:
            pass

        self._close_db()

    def _connect_db(self, name=None):
        if name is not None:
            self._conn = psycopg2.connect(host=self._config.pg_host, port=self._config.pg_port,
                                    user=self._config.pg_user, password=self._config.pg_pass,
                                    dbname=name)
        else:
            self._conn = psycopg2.connect(host=self._config.pg_host, port=self._config.pg_port,
                                    user=self._config.pg_user, password=self._config.pg_pass)

        self._conn.autocommit = True
        self._cur = self._conn.cursor()

    def _insert_data(self, data):
        self._cur.execute("insert into %s(%s) values('%s') on conflict(%s) do update set %s='%s';" %
                         (self._table, ','.join(data.keys()), "','".join(data.values()), Schema.URL, Schema.COMMIT,
                          data[Schema.COMMIT]))

        self._cur.execute("insert into %s(%s) values('%s') on conflict(%s) do update set %s='%s';" %
                         (self._table, ','.join(data.keys()), "','".join(data.values()), Schema.URL, Schema.DATE,
                          data[Schema.DATE]))

    def _close_db(self):
        self._cur.close()
        self._conn.close()
