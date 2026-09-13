from app.store.statistic.prepare import statistics_prepare
from services.db import Db
from models.statistic import Statistic

def statistics_store():
    Db.save_many_by_keys(
        model=Statistic,
        records=statistics_prepare(),
        keys=['match_id','player_id','team_id']
    )

if __name__ == "__main__": statistics_store()