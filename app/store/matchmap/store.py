from app.store.matchmap.prepare import match_maps_prepare
from services.db import Db
from models.matchmap import MatchMap

def match_maps_store():
    Db.save_many_by_keys(model=MatchMap,records=match_maps_prepare(),keys=['match_id','map_id'])

if __name__ == "__main__": match_maps_store()