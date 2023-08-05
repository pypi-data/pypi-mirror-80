
class RedisSetManager(object):
    __redis = None

    @classmethod
    def config(cls, redis):
        cls.__redis = redis
        return cls

    @classmethod
    def add(cls, key, *values):
        return cls.__redis.sadd(key, *values)

    @classmethod
    def remove(cls, key, *values):
        return cls.__redis.srem(key, *values)

    @classmethod
    def count(cls, key):
        return cls.__redis.scard(key)

    @classmethod
    def difference(cls, keys, *args):
        return cls.__redis.sdiff(keys, *args)

    @classmethod
    def generate_difference(cls, gen_key, *keys):
        return cls.__redis.sdiffstore(gen_key, keys)

    @classmethod
    def intersection(cls, *keys):
        return cls.__redis.sinter(keys)

    @classmethod
    def generate_intersection(cls, gen_key, *keys):
        return cls.__redis.sinterstore(gen_key, keys)

    @classmethod
    def union(cls, *keys):
        return cls.__redis.sunion(*keys)

    @classmethod
    def generate_union(cls, gen_key, *keys):
        return cls.__redis.sunionstore(gen_key, keys)

    @classmethod
    def is_member(cls, value, key):
        return cls.__redis.sismember(key, value)

    @classmethod
    def move(cls, value, from_, to_):
        return cls.__redis.smove(from_, to_, value)

    @classmethod
    def pop(cls, key, count=None):
        return cls.__redis.spop(key, count)

    @classmethod
    def get_all_value(cls, key):
        return cls.__redis.smembers(key)

    @classmethod
    def get_random_value(cls, key, count=None):
        return cls.__redis.srandmember(key, count)

    @classmethod
    def scan(cls, key, cursor=0, pattern=None, count=None):
        return cls.__redis.sscan(key, cursor, pattern, count)

