from services.db import Db
from models.maps import Map

def map_store(map_data):
    return Db.save(model=Map,data=map_data,key='name')