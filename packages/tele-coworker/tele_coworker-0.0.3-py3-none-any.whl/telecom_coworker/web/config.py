import os


class Config(object):
    ZK_NAMESPACE = os.environ.get('ZK_NAMESPACE', 'basic')
    ZK_HOSTS = os.environ.get('ZK_HOSTS', 'localhost:2181')
