from graphene import ObjectType, String, Int, Schema, List
from lib import RedisBD
from flask import Flask
from flask_graphql import GraphQLView

class PlayerScore(ObjectType):
    name=String()
    score=Int()
    def resolve_name(playerScore, info):
        return playerScore.name
    
    def resolve_score(playerScore, info):
        return playerScore.score

bd = RedisBD()

class GameSession(ObjectType):
    global bd
    
    id=Int()
    label=String()
    timestamp=Int()
    scoreboard=List(PlayerScore)
    
    def resolve_id(gameSession, info):
        return gameSession.id
    
    def resolve_label(gameSession, info):
        return gameSession.label.decode("utf-8") 
    
    def resolve_timestamp(gameSession, info):
        return gameSession.timestamp
    
    def resolve_scoreboard(gameSession, info):
        return bd.get_game_session(gameSession.id.decode("utf-8") )


class Query(ObjectType):
    global bd
    recent_sessions = List(GameSession)
    active_sessions = List(GameSession)
    
    def resolve_recent_sessions(root, info):
        return bd.get_active_sessions()
    
    def resolve_active_sessions(root, info):
        return bd.get_active_sessions() 

schema = Schema(query=Query)
app = Flask(__name__)
app.add_url_rule(
  '/',
  view_func=GraphQLView.as_view('graphql', schema=schema, graphiql=True)
)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)
