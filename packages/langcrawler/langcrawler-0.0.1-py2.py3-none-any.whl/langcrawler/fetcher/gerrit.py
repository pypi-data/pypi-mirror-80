# -*- coding: utf-8 -*-

from ..request.request import Request, RequestException
from ..schema.schema import Schema


class GerritException(Exception):
    def __init__(self, info):
        super().__init__(self)
        self._info = info

    def __str__(self):
        return self._info


class Gerrit(object):
    _url = 'https://gerrit-review.googlesource.com/projects/'

    def __init__(self):
        try:
            self._request = Request(retry=1, timeout=None)
        except RequestException as e:
            raise GerritException('init failed %s' % str(e))

    def run(self, langs, count):
        result = []

        try:
            buf = self._request.run(self._url+'?n=%d' % count)
            for key, val in buf.items():
                result.append(self._schema(key, val))
        except RequestException as e:
            raise GerritException('run failed %s' % str(e))

        return result

    def _schema(self, repo, data):
        schema = Schema()
        schema.clone = data['web_links'][0]['url']
        revision, date = self._commit(data['id'])
        schema.commit = revision
        schema.date = date
        schema.host = 'https://gerrit-review.googlesource.com'
        schema.language = ''
        schema.repo = repo
        schema.url = data['web_links'][0]['url']

        return schema

    def _commit(self, repo):
        try:
            buf = self._request.run(self._url+repo+'/branches')
        except RequestException as e:
            raise GerritException('branch failed %s' % str(e))

        revision = ''

        for item in buf:
            ref = item.get('ref', None)
            if ref == 'refs/heads/master':
                revision = item['revision']
                break

        try:
            buf = self._request.run(self._url+repo+'/commits/'+revision)
        except RequestException as e:
            raise GerritException('commit failed %s' % str(e))

        return revision, buf['committer']['date']
