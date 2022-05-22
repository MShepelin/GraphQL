import redis
from collections import namedtuple

Session=namedtuple("Session",['id','label','timestamp'])

class RedisBD:
    def __init__(self):
        self.connection = redis.Redis()
        self.connection.hmset("active_sessions_0", Session(300, "John", 23)._asdict())
        self.connection.hmset("active_sessions_1", Session(2323, "Jerry", 24)._asdict())
        self.connection.hmset("active_sessions_2", Session(1212, "Jason", 25)._asdict())
        self.connection.hmset("active_sessions_3", Session(4334, "Bruce", 28)._asdict())

    def get_active_sessions(self):
        result = []
        for i in range(4):
            keys = self.connection.hgetall(f"active_sessions_{i}")
            result.append(Session(*keys.values()))
        
        return result
