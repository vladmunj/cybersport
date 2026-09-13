from services.db import Db
from models.player import Player

def player_store(player_data):
    return Db.save(model=Player,data=player_data,key='nickname')