# -*- coding: utf-8 -*-

import sys

from .cmd.argument import Argument
from .cmd.banner import BANNER
from .config.config import Config, ConfigException
from .logger.logger import Logger
from .scheduler.scheduler import Scheduler, SchedulerException


def main():
    print(BANNER)

    argument = Argument()
    arg = argument.parse(sys.argv)

    try:
        config = Config()
        config.lang(arg.lang_type)
        config.postgres(arg.pg_address, arg.pg_login)
        config.redis(arg.redis_address, arg.redis_pass)
        config.repo(arg.repo_count, arg.repo_host)
    except ConfigException as e:
        Logger.error(str(e))
        return -1

    try:
        scheduler = Scheduler(config)
        scheduler.run()
    except SchedulerException as e:
        Logger.error(str(e))
        return -2

    return 0
