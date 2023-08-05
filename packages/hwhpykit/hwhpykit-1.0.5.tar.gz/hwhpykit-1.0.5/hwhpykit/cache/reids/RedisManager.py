import redis
from hwhpykit.cache.reids.base.RedisGEO import RedisGEO
from hwhpykit.cache.reids.base.RedisSetManager import RedisSetManager
from hwhpykit.cache.reids.base.RedisHashManager import RedisHashManager
from hwhpykit.cache.reids.base.RedisListManager import RedisListManager
from hwhpykit.cache.reids.base.RedisZSetManager import RedisZSetManager
from hwhpykit.cache.reids.base.RedisStringManager import RedisStringManager
from hwhpykit.cache.reids.action.RedisServer import RedisServer
from hwhpykit.cache.reids.action.RedisSubscriber import RedisSubscriber
from hwhpykit.cache.reids.action.RedisTransaction import RedisTransaction


class RedisManager(object):
    __redis = None
    __pool = None
    __tag = ""

    string = RedisStringManager
    hash = RedisHashManager
    set = RedisSetManager
    zset = RedisZSetManager
    list = RedisListManager
    geo = RedisGEO
    transaction = RedisTransaction
    subscriber = RedisSubscriber
    server = RedisServer

    @classmethod
    def config(cls, host='127.0.0.1', port=6379, db=0, password=''):
        cls.__pool = redis.ConnectionPool(host=host, port=port, db=db, password=password)
        cls.__redis = redis.Redis(connection_pool=cls.__pool)

        cls.geo = RedisGEO.config(cls.__redis)
        cls.set = RedisSetManager.config(cls.__redis)
        cls.hash = RedisHashManager.config(cls.__redis)
        cls.zset = RedisZSetManager.config(cls.__redis)
        cls.list = RedisListManager.config(cls.__redis)
        cls.string = RedisStringManager.config(cls.__redis)

        cls.transaction = RedisTransaction.config(cls.__redis)
        cls.subscriber = RedisSubscriber.config(cls.__redis)
        cls.server = RedisServer.config(cls.__redis)
        return cls


