from graphene import ObjectType, String, Int, Schema, Field, List
from server_back import RedisBD

class GameSession(ObjectType):
    id=Int()
    label=String()
    timestamp=Int()
    
    def resolve_id(gameSession, info):
        return gameSession.id
    
    def resolve_label(gameSession, info):
        return gameSession.label.decode("utf-8") 
    
    def resolve_timestamp(gameSession, info):
        return gameSession.timestamp
    
bd = RedisBD()

class Query(ObjectType):
    global bd
    recent_sessions = List(GameSession)
    active_sessions = List(GameSession)
    
    def resolve_recent_sessions(root, info):
        return bd.get_active_sessions() # TODO change
    
    def resolve_active_sessions(root, info):
        return bd.get_active_sessions() 

schema = Schema(query=Query)
result = schema.execute('{ recentSessions { id label } }')
print(result.data)
