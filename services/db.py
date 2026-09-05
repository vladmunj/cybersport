from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.config import (
    POSTGRES_HOST,POSTGRES_PORT,POSTGRES_USER,POSTGRES_PASSWORD,POSTGRES_DB
)

class Db:
    __instance = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = object.__new__(cls)
        return cls.__instance

    def __init__(self):
        if hasattr(self, "_initialized"): return
        self._initialized = True
        db_url = self.__init_db_url()
        self.engine = create_engine(
            db_url,
            pool_pre_ping=True,
        )
        self.session_factory = sessionmaker(
            bind=self.engine,
            autoflush=False,
            autocommit=False,
        )

    def __init_db_url(self):
        return (
            f"postgresql+psycopg://"
            f"{POSTGRES_USER}:{POSTGRES_PASSWORD}"
            f"@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"
        )