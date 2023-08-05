

class RedisSubscriber(object):
    __redis = None
    __pool = None

    @classmethod
    def config(cls, redis, key=None):
        cls.__redis = redis
        cls.__key = key
        return cls

    @classmethod
    def subscribe_by_pattern(cls, *patterns):
        cls.__redis.psubscribe(*patterns)

    @classmethod
    def unsubscribe_by_pattern(cls, *patterns):
        cls.__redis.punsubscribe(*patterns)

    @classmethod
    def subscribe_by_channel(cls, *channels):
        cls.__redis.subscribe(*channels)

    @classmethod
    def unsubscribe_by_channel(cls, *channels):
        cls.__redis.unsubscribe(*channels)

    @classmethod
    def scribe_status(cls, *channels):
        cls.__redis.pubsub(*channels)

    @classmethod
    def publish_to_channel(cls, channel, message):
        cls.__redis.publish(channel, message)

