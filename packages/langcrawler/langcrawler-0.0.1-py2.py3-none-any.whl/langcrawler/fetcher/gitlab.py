# -*- coding: utf-8 -*-

from ..request.request import Request, RequestException
from ..schema.schema import Schema


class GitLabException(Exception):
    def __init__(self, info):
        super().__init__(self)
        self._info = info

    def __str__(self):
        return self._info


class GitLab(object):
    _url = ''

    def __init__(self):
        try:
            self._request = Request(retry=1, timeout=None)
        except RequestException as e:
            raise GitLabException('init failed %s' % str(e))

    def run(self, langs, count):
        result = []

        for lang in langs:
            try:
                buf = self._request.run(self._url % (lang, count))
            except RequestException as e:
                raise GitLabException('run failed %s' % str(e))
            for item in buf:
                result.append(self._schema(item))

        return result

    def _schema(self, data):
        schema = Schema()
        schema.clone = ''
        buf = self._commit(data)
        schema.commit = ''
        schema.date = ''
        schema.host = 'https://gitlab.com'
        schema.language = ''
        schema.repo = ''
        schema.url = ''

        return schema

    def _commit(self, url):
        try:
            buf = self._request.run(url)
        except RequestException as e:
            raise GitLabException('commit failed %s' % str(e))

        return buf
