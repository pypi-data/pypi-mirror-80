


# hwhpykit

- 依据个人习惯封装的常用第三方库
- 依赖的第三方库：
  - [Redis](https://github.com/andymccurdy/redis-py) 

## Main function

- Cache
    - Redis-client 
        - string
        - list
        - hash 
        - set 
        - zset
        - geo
        - server
        - subscribe
        - transaction

- Buffer
> Kafka-client
>
>RabbitMQ-client
>
>RocketMQ-client

- DataBase
> MySQL-client
>
> PostgreSQL-client


## Cache

### Redis-client

> from hwhpykit.cache.reids.RedisManager import RedisManager
>
> RedisManager.config(host="127.0.0.1", db=0)

#### string
> RedisManager.string.set("reids", "value")
>
> RedisManager.string.set_keys({"a":1, "b": 2})
>
> RedisManager.string.set_range("redis", 6, "666")
>
> RedisManager.string.set_not_exist_key('11', "1222")
>
> RedisManager.string.append('redis', '---')
> 
> key = 'redis'
>
> r = RedisManager.string.get(key)
>
> r = RedisManager.string.get_len(key)
>
>r = RedisManager.string.get_range(key, 0, -1)
>
>r = RedisManager.string.get_values(['11', "1222"])
>
>RedisManager.string.set('2', '0')
>
>RedisManager.string.increase('2')
>
>RedisManager.string.increase('2', -100000)
>
>r = RedisManager.string.get('2')
>
#### hash

>key = "redis-hash"
>
>RedisManager.hash.set_map(key, {"louis1": "1", "louis2": "2"})
>
>RedisManager.hash.set_value(key, "louis3", "3")
>
>RedisManager.hash.set_not_exits_value(key, "louis3", "4")
>
>r = RedisManager.hash.get_all(key)
>
>RedisManager.hash.delete_field(key, "louis1")
>
>RedisManager.hash.increase_field_int(key, "louis3", 100)
>
>RedisManager.hash.increase_field_float(key, "louis2", 100.000001)
>
>r = RedisManager.hash.get_all(key)
>
>r = RedisManager.hash.get_all_keys(key)
>
>r = RedisManager.hash.get_all_values(key)
>
>r = RedisManager.hash.get_all_key_count(key)
>
>r = RedisManager.hash.get_value_bytes_len(key, "louis2")
>
>r = RedisManager.hash.scan(key, cursor=0, pattern="louis2", count=10)
>
#### set
> key = "test_set"
> key1 = "test_set_1"
> key2 = "test_set_2"
> key3 = "test_set_3"
> 
> RedisManager.set.add(key1, 1, 2, 3)
> RedisManager.set.add(key2, 1, 2, 3, 4, 5, 6)
> RedisManager.set.add(key3, 1, 2, 3, 7, 8, 9)
> 
> RedisManager.set.remove(key, 1, 2, 3)
> 
> RedisManager.set.count(key)
> 
> RedisManager.set.difference(key2, key3)
> 
> RedisManager.set.intersection(key2, key3)
> 
> RedisManager.set.union(key2, key3)
>
> RedisManager.set.is_member(3, key3)
> 
> RedisManager.set.get_all_value(key3)
> 

### GEO
> key = "test-geo-key"
>
> RedisManager.geo.add(key, 1, 1, 'a1')
>
> RedisManager.geo.add(key, 2, 1, 'a2')
>
> RedisManager.geo.get_location(key, 'a')
>
> distance = RedisManager.geo.distance(key, 'a1', 'a2')
>
> locations = RedisManager.geo.radius_locations(key, 0, 0,300, withdist=True, withcoord=True, sort='ASC')
>
> locations = RedisManager.geo.radius_locations_by_member(key, 'a1', 300, withdist=True, withcoord=True, sort='ASC')
>
> location_hash = RedisManager.geo.hash(key, 'a1', 'a2')
>

### Database



