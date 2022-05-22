import redis
from collections import namedtuple
import json

Session=namedtuple("Session",['id','label','timestamp'])
ScoreBoardRow=namedtuple("ScoreBoardRow", ["name", "score"])

class RedisBD:
    def __init__(self):
        self.connection = redis.Redis()
        self.connection.hmset("active_sessions_0", Session(0, "BestGame", 10808080)._asdict())
        self.connection.hmset("active_sessions_1", Session(1, "JerryBirthday", 10808120)._asdict())
        self.connection.hmset("active_sessions_2", Session(2, "Room5", 10808000)._asdict())
        self.connection.hmset("active_sessions_3", Session(3, "RandomName123", 10808100)._asdict())
        
        if not self.connection.exists("active_sessions_0_score"):
            self.connection.lpush("active_sessions_0_score", json.dumps(
                ScoreBoardRow("Borg", 30)._asdict()
            ))
            self.connection.lpush("active_sessions_0_score", json.dumps(
                ScoreBoardRow("Dorg", 100)._asdict()
            ))
        
        if not self.connection.exists("active_sessions_3_score"):
            self.connection.lpush("active_sessions_3_score", json.dumps(
                ScoreBoardRow("Bro", 90)._asdict()
            ))
            self.connection.lpush("active_sessions_3_score", json.dumps(
                ScoreBoardRow("Dre", 40)._asdict()
            ))

    def get_active_sessions(self):
        result = []
        for i in range(4):
            keys = self.connection.hgetall(f"active_sessions_{i}")
            result.append(Session(*keys.values()))
        
        return result
    
    def get_game_session(self, id):
        if not self.connection.exists(f"active_sessions_{id}_score"):
            return []
        else:
            result = self.connection.lrange(f"active_sessions_{id}_score", 0, -1)
            for i in range(len(result)):
                result[i] = ScoreBoardRow(**json.loads(result[i]))
            print(len(result))
            return result
