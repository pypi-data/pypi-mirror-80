# -*- coding: utf-8 -*-

class ConfigException(Exception):
    def __init__(self, info):
        super().__init__(self)
        self._info = info

    def __str__(self):
        return self._info


class Config(object):
    hosts = ['gerrit', 'github', 'gitlab']
    langs = ['go', 'javascript', 'php', 'python', 'rust', 'typescript']

    def __init__(self):
        self.lang_type = []

        self.pg_host = '127.0.0.1'
        self.pg_port = '5432'
        self.pg_user = 'postgres'
        self.pg_pass = 'postgres'

        self.redis_host = '127.0.0.1'
        self.redis_port = '6379'
        self.redis_pass = 'redis'

        self.repo_count = 1
        self.repo_host = []

    def lang(self, _type):
        if len(_type.strip()) == 0:
            raise ConfigException('type invalid: %s' % _type)

        buf = _type.split(',')
        for item in buf:
            if item.strip() not in self.langs:
                raise ConfigException('type invalid: %s' % item)
            self.lang_type.append(item.strip())

    def postgres(self, address, login):
        if len(address.strip()) == 0:
            raise ConfigException('address invalid: %s' % address)

        if len(login.strip()) == 0:
            raise ConfigException('login invalid: %s' % login)

        host, port = address.split(':')
        if len(host.strip()) != 0:
            self.pg_host = host
        if len(port.strip()) != 0:
            self.pg_port = port

        user, _pass = login.split('/')
        if len(user.strip()) != 0:
            self.pg_user = user
        if len(_pass.strip()) != 0:
            self.pg_pass = _pass

    def redis(self, address, _pass):
        if len(address.strip()) == 0:
            raise ConfigException('address invalid: %s' % address)

        if len(_pass.strip()) == 0:
            raise ConfigException('pass invalid: %s' % _pass)

        host, port = address.split(':')
        if len(host.strip()) != 0:
            self.redis_host = host
        if len(port.strip()) != 0:
            self.redis_port = port

        if len(_pass.strip()) != 0:
            self.redis_pass = _pass

    def repo(self, count, host):
        if count <= 0:
            raise ConfigException('count invalid: %d' % count)

        if len(host.strip()) == 0:
            raise ConfigException('host invalid: %s' % host)

        self.repo_count = count

        buf = host.split(',')
        for item in buf:
            if item.strip() not in self.hosts:
                raise ConfigException('host invalid: %s' % item)
            self.repo_host.append(item.strip())
