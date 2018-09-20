from os.path import dirname, abspath
from fabric.api import local, lcd


BASE_DIR = dirname(abspath(__file__))


def test():
    local("tox")


def run():
    local('python {}/manage.py run'.format(BASE_DIR))


def shell():
    local('python {}/manage.py shell'.format(BASE_DIR))
