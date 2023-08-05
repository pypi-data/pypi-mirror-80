

class RedisListManager(object):
    __redis = None
    __key = None

    @classmethod
    def config(cls, redis, key=None):
        cls.__redis = redis
        cls.__key = key
        return cls

    @classmethod
    def right_push(cls, key, *values):
        return cls.__redis.rpush(key, *values)

    @classmethod
    def right_exist_push(cls, key, value):
        return cls.__redis.rpushx(key, value)

    @classmethod
    def left_push(cls, key, *values):
        return cls.__redis.lpush(key, *values)

    @classmethod
    def left_exist_push(cls, key, value):
        return cls.__redis.lpushx(key, value)

    @classmethod
    def insert(cls, key, value, before=True, tag=""):
        if before:
            return cls.__redis.linsert(key, "before", tag, value)
        else:
            return cls.__redis.linsert(key, "after", tag, value)

    @classmethod
    def remove_value(cls, key, value, count):
        return cls.__redis.lrem(key,count, value)

    @classmethod
    def right_pop(cls, key):
        return cls.__redis.rpop(key)

    @classmethod
    def left_pop(cls, key):
        return cls.__redis.lpop(key)

    @classmethod
    def right_pop_left_push(cls, origin, target):
        return cls.__redis.rpoplpush(origin, target)

    @classmethod
    def b_right_pop(cls, keys, timeout=0):
        return cls.__redis.brpop(keys, timeout)

    @classmethod
    def b_left_pop(cls, keys, timeout):
        return cls.__redis.blpop(keys, timeout)

    @classmethod
    def b_right_pop_left_push(cls, right_key, left_key, timeout=0):
        return cls.__redis.brpoplpush(right_key, left_key, timeout)

    @classmethod
    def left_set(cls, key, value, index):
        return cls.__redis.lset(key, index, value)

    @classmethod
    def trim_list(cls, key, start, end):
        return cls.__redis.ltrim(key, start, end)

    @classmethod
    def get_index(cls, key, index):
        return cls.__redis.lindex(key, index)

    @classmethod
    def get_range(cls, key, start, end):
        return cls.__redis.lrange(key, start, end)

    @classmethod
    def get_list_count(cls, key):
        return cls.__redis.llen(key)

