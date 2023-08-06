# -*- coding: utf-8 -*-

from ..request.request import Request, RequestException


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
        # TODO
        result = []

        return result
