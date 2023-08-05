

class RedisZSetManager(object):
    __redis = None
    __pool = None

    @classmethod
    def config(cls, redis, key=None):
        cls.__redis = redis
        cls.__key = key
        return cls

    @classmethod
    def add(cls, key, members_score):
        return cls.__redis.zadd(key, members_score)

    @classmethod
    def count(cls, key):
        """总数量"""
        return cls.__redis.zcard(key)

    @classmethod
    def increment_member(cls, key, increment, member):
        return cls.__redis.zincrby(key, increment, member)

    @classmethod
    def range_count(cls, key, min_element="-", max_element="+"):
        """ 两个成员之间元素的数量 """
        return cls.__redis.zlexcount(key, min=min_element, max=max_element)

    @classmethod
    def range_values(cls, key, start, stop, desc=False, withscores=False):
        """ 在集合中元素的排名 """
        return cls.__redis.zrange(key, start, stop, desc=desc, withscores=withscores)

    @classmethod
    def range_values_by_lex(cls, key, min_element="-", max_element="+", desc=False):
        """ 两个成员之间的元素 """
        if desc:
            return cls.__redis.zrevrangebylex(key, min_element, max_element)
        else:
            return cls.__redis.zrangebylex(key, min_element, max_element)

    @classmethod
    def range_values_by_score(cls, key, min_score, max_score, withscores=False, desc=False):
        """ 两个成员之间的元素 """
        if desc:
            return cls.__redis.zrevrangebyscore(key, min_score, max_score, withscores=withscores)
        else:
            return cls.__redis.zrangebyscore(key, min_score, max_score, withscores=withscores)

    @classmethod
    def rank(cls, key, member, desc=False):
        """ 在集合中元素的排名 """
        if desc:
            return cls.__redis.zrevrank(key, member)
        else:
            return cls.__redis.zrank(key, member)

    @classmethod
    def remove(cls, key, *members):
        return cls.__redis.zrem(key, *members)

    @classmethod
    def remove_range_by_lex(cls, key, min_element, max_element):
        return cls.__redis.zremrangebylex(key, min=min_element, max=max_element)

    @classmethod
    def remove_range_by_score(cls, key, min_score, max_score):
        return cls.__redis.zremrangebyscore(key, min_score, max_score)

    @classmethod
    def remove_range_by_rank(cls, key, min_, max_):
        return cls.__redis.zremrangebyrank(key, min_, max_)

    @classmethod
    def get_score(cls, key, member):
        return cls.__redis.zscore(key, member)

    @classmethod
    def generate_difference(cls, gen_key, keys):
        return cls.__redis.zinterstore(gen_key, keys=keys)

    @classmethod
    def generate_union(cls, key, *keys):
        return cls.__redis.zunionstore(key, *keys)

    @classmethod
    def scan(cls, key, cursor=0, match=None, count=None):
        return cls.__redis.zscan(key, cursor, match, count)
