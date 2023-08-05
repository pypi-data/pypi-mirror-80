

class RedisTransaction(object):
    __redis = None
    __pool = None

    @classmethod
    def config(cls, redis, key=None):
        cls.__redis = redis
        cls.__key = key
        return cls

    @classmethod
    def discard(cls): ...

    @classmethod
    def exec(cls): ...

    @classmethod
    def multi(cls): ...

    @classmethod
    def unwatch(cls): ...

    @classmethod
    def watch(cls, keys): ...

