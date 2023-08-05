

class RedisStringManager(object):
    __redis = None
    __key = None

    @classmethod
    def config(cls, redis, key=None):
        cls.__redis = redis
        cls.__key = key
        return cls

    # Set ----------------------------------------------

    @classmethod
    def set_not_exist_key(cls, key, value):
        return cls.__redis.setnx(key, value)

    @classmethod
    def set_not_exist_keys(cls, kv_list):
        return cls.__redis.msetnx(kv_list)

    @classmethod
    def set(cls, key, value, seconds=None):
        if seconds is None:
            return cls.__redis.set(key, value)
        else:
            if seconds > 0:
                return cls.__redis.setex(key, seconds, value)
            else:
                return cls.__redis.psetex(key, seconds * 1000, value)

    @classmethod
    def set_keys(cls, kv_list):
        return cls.__redis.mset(kv_list)

    @classmethod
    def set_bit(cls, key, index, bit):
        return cls.__redis.setbit(key, index, bit)

    @classmethod
    def set_range(cls, key, start, value):
        return cls.__redis.setrange(key, start, value)

    # Get ----------------------------------------------

    @classmethod
    def get(cls, key, start=None, end=None):
        if start is None and end is None:
            return cls.__redis.get(key)
        else:
            return cls.__redis.getrange(key, start, end)

    @classmethod
    def get_len(cls, key):
        return cls.__redis.strlen(key)

    @classmethod
    def get_range(cls, key, start, end):
        return cls.__redis.getrange(key, start, end)

    @classmethod
    def get_set(cls, key, new_value):
        return cls.__redis.getset(key, new_value)

    @classmethod
    def get_bit(cls, key, index):
        return cls.__redis.getbit(key, index)

    @classmethod
    def get_values(cls, keys):
        return cls.__redis.mget(keys)

    # Other Options ----------------------------------------------

    @classmethod
    def append(cls, key, value):
        return cls.__redis.append(key, value)

    @classmethod
    def increase(cls, key, count=None):
        if count is None:
            return cls.__redis.incr(key)
        else:
            return cls.__redis.incrby(key, count)

    @classmethod
    def decrease(cls, key, count=None):
        if count is None:
            return cls.__redis.decr(key)
        else:
            return cls.__redis.decrby(key, count)





