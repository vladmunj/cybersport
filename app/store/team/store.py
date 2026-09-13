from services.db import Db
from models.team import Team

def team_store(team_data):
    return Db.save(model=Team,data=team_data,key='slug')