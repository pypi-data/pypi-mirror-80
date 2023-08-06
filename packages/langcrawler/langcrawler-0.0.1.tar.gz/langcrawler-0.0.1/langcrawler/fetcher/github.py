# -*- coding: utf-8 -*-

from ..request.request import Request, RequestException
from ..schema.schema import Schema


class GitHubException(Exception):
    def __init__(self, info):
        super().__init__(self)
        self._info = info

    def __str__(self):
        return self._info


class GitHub(object):
    _url = 'https://api.github.com/search/repositories?q=archived:false+is:public+language:%s+mirror:false+stars:>=1000&sort=stars&order=desc&page=1&per_page=%s'

    def __init__(self):
        try:
            self._request = Request(retry=1, timeout=None)
        except RequestException as e:
            raise GitHubException('init failed %s' % str(e))

    def run(self, langs, count):
        result = []

        for lang in langs:
            try:
                buf = self._request.run(self._url % (lang, count))
            except RequestException as e:
                raise GitHubException('run failed %s' % str(e))
            for item in buf['items']:
                result.append(self._schema(item))

        return result

    def _schema(self, data):
        schema = Schema()
        schema.clone = data['clone_url']
        buf = self._commit(data['commits_url'].replace('{/sha}', ''))
        schema.commit = buf['sha']
        schema.date = buf['commit']['committer']['date']
        schema.host = 'https://github.com'
        schema.language = data['language']
        schema.repo = data['full_name']
        schema.url = data['html_url']

        return schema

    def _commit(self, url):
        try:
            buf = self._request.run(url)
        except RequestException as e:
            raise GitHubException('commit failed %s' % str(e))

        return buf[0]
