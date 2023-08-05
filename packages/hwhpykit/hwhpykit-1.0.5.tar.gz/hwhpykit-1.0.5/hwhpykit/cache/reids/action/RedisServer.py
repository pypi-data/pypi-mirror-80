

class RedisServer(object):
    __redis = None

    @classmethod
    def config(cls, redis):
        cls.__redis = redis
        return cls

    # @classmethod
    # def aof_save(cls): ...
    #
    # @classmethod
    # def bg_save(cls): ...

    @classmethod
    def client_kill(cls, address):
        return cls.__redis.client_kill(address)

    @classmethod
    def clients(cls, type='normal'):
        return cls.__redis.client_list(type)

    @classmethod
    def unwatch(cls): ...

    @classmethod
    def watch(cls, keys): ...
