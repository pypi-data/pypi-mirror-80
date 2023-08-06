# langcrawler

[![PyPI](https://img.shields.io/pypi/v/langcrawler.svg?color=brightgreen)](https://pypi.org/project/langcrawler/)
[![Travis](https://travis-ci.com/craftslab/langcrawler.svg?branch=master)](https://travis-ci.com/craftslab/langcrawler)
[![Coverage](https://coveralls.io/repos/github/craftslab/langcrawler/badge.svg?branch=master)](https://coveralls.io/github/craftslab/langcrawler?branch=master)
[![License](https://img.shields.io/github/license/craftslab/langcrawler.svg?color=brightgreen)](https://github.com/craftslab/langcrawler/blob/master/LICENSE)



*langcrawler* is a language crawler written in Python.



## Requirement

- PostgreSQL >= 12.4
- Python >= 3.8
- Redis >= 6.0



## Installation

### Ubuntu

```bash
apt update
apt install -y python3-dev python3-pip python3-setuptools
pip install langcrawler
```

### Windows

```
# Install Python, Microsoft Visual C++ and Windows SDK
pip install langcrawler
```



## Updating

```bash
pip install langcrawler --upgrade
```



## Running

```bash
langcrawler \
    --lang-type go,javascript,php,python,rust,typescript \
    --pg-address 127.0.0.1:5432 \
    --pg-login postgres/postgres \
    --redis-address 127.0.0.1:6379 \
    --redis-pass redis \
    --repo-count 10 \
    --repo-host gerrit,github,gitlab
```



## Usage

```bash
usage: langcrawler [-h] [--lang-type LANG_TYPE] [--pg-address PG_ADDRESS]
                   [--pg-login PG_LOGIN] [--redis-address REDIS_ADDRESS]
                   [--redis-pass REDIS_PASS] [--repo-count REPO_COUNT]
                   [--repo-host REPO_HOST] [-v]

Language Crawler

optional arguments:
  -h, --help            show this help message and exit
  --lang-type LANG_TYPE
                        language type
  --pg-address PG_ADDRESS
                        postgres address (host:port)
  --pg-login PG_LOGIN   postgres login (user/pass)
  --redis-address REDIS_ADDRESS
                        redis address (host:port)
  --redis-pass REDIS_PASS
                        redis pass
  --repo-count REPO_COUNT
                        repository count
  --repo-host REPO_HOST
                        repository host
  -v, --version         show program's version number and exit
```



## License

Project License can be found [here](https://github.com/craftslab/langcrawler/blob/master/LICENSE).



## Reference

- [Search on Gerrit](https://gerrit-documentation.storage.googleapis.com/Documentation/3.2.3/rest-api.html)
- [Search on GitHub](https://developer.github.com/v3/search/)
- [Search on GitLab](https://docs.gitlab.com/ee/api/api_resources.html)
