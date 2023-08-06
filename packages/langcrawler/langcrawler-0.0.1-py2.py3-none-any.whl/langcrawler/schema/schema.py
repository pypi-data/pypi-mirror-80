# -*- coding: utf-8 -*-

class SchemaException(Exception):
    def __init__(self, info):
        super().__init__(self)
        self._info = info

    def __str__(self):
        return self._info


class Schema(object):
    def __init__(self):
        self.clone = ''
        self.commit = ''
        self.date = ''
        self.host = ''
        self.language = ''
        self.repo = ''
        self.url = ''

    def dump(self):
        print('clone: %s' % self.clone)
        print('commit: %s' % self.commit)
        print('date: %s' % self.date)
        print('host: %s' % self.host)
        print('language: %s' % self.language)
        print('repo: %s' % self.repo)
        print('url: %s' % self.url)
