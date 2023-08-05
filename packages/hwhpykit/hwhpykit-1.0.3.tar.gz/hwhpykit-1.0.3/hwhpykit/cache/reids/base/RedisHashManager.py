

class RedisHashManager(object):
    __redis = None
    __key = None

    @classmethod
    def config(cls, redis, key=None):
        cls.__redis = redis
        cls.__key = key
        return cls

    @classmethod
    def set_map(cls, key, dic):
        cls.__redis.hset(key, mapping=dic)

    @classmethod
    def set_value(cls, key, field, value):
        cls.__redis.hset(key, key=field, value=value)

    @classmethod
    def set_not_exits_value(cls, key, field, value):
        cls.__redis.hsetnx(key, key=field, value=value)

    @classmethod
    def delete_field(cls, key, field):
        cls.__redis.hdel(key, field)

    @classmethod
    def increase_field_int(cls, key, field, increment=1):
        cls.__redis.hincrby(key, field, increment)

    @classmethod
    def increase_field_float(cls, key, field, increment=1.0):
        cls.__redis.hincrbyfloat(key, field, increment)

    @classmethod
    def exist_field(cls, key, field):
        return cls.__redis.hexists(key, field)

    @classmethod
    def get_value(cls, key, field):
        return cls.__redis.hget(key, field)

    @classmethod
    def get_values(cls, keys):
        return cls.__redis.hmget(keys)

    @classmethod
    def get_all(cls, key):
        return cls.__redis.hgetall(key)

    @classmethod
    def get_all_values(cls, key):
        return cls.__redis.hvals(key)

    @classmethod
    def get_all_keys(cls, key):
        return cls.__redis.hkeys(key)

    @classmethod
    def get_all_key_count(cls, key):
        return cls.__redis.hlen(key)

    @classmethod
    def get_value_bytes_len(cls, key, field):
        return cls.__redis.hstrlen(key, key=field)

    @classmethod
    def scan(cls, key, cursor, pattern, count):
        return cls.__redis.hscan(key, cursor, pattern, count)



