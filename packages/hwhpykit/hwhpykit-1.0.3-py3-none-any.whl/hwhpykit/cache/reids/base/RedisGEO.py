

class RedisGEO(object):
    __redis = None
    __pool = None

    @classmethod
    def config(cls, redis, key=None):
        cls.__redis = redis
        cls.__key = key
        return cls

    @classmethod
    def add(cls, key, *values):
        return cls.__redis.geoadd(key, *values)

    @classmethod
    def get_location(cls, key, member):
        return cls.__redis.geopos(key, member)

    @classmethod
    def distance(cls, key, member1, member2, unit='km'):
        return cls.__redis.geodist(key, member1, member2, unit=unit)

    @classmethod
    def radius_locations(cls, key, longitude, latitude, radius,
                         unit='km', withdist=False, withcoord=False,
                         count=None,sort=None):
        return cls.__redis.georadius(name=key, longitude=longitude, latitude=latitude,
                                     radius=radius, unit=unit, withdist=withdist,
                                     withcoord=withcoord, count=count, sort=sort)

    @classmethod
    def radius_locations_by_member(cls, key, member, radius,
                         unit=None, withdist=False, withcoord=False,
                         count=None,sort=None):
        return cls.__redis.georadiusbymember(name=key, member=member,radius=radius,
                                             unit=unit, withdist=withdist,
                                             withcoord=withcoord, count=count, sort=sort)

    @classmethod
    def hash(cls, key, *members):
        return cls.__redis.geohash(key, *members)



