from app.store.match.prepare import matches_prepare
from services.db import Db
from models.match import Match

def matches_store():
    Db.save_many(model=Match,records=matches_prepare(),key='external_id')

if __name__ == "__main__": matches_store()