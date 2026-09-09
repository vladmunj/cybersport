from sqlalchemy import create_engine, select
from sqlalchemy.engine import URL
from sqlalchemy.orm import sessionmaker
from app.config import (
    POSTGRES_HOST,POSTGRES_PORT,POSTGRES_USER,POSTGRES_PASSWORD,POSTGRES_DB
)
from typing import Any, Type

class Db:
    __instance = None
    _engine = None
    _session_factory = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = object.__new__(cls)
        return cls.__instance

    def __init__(self):
        if hasattr(self, "_initialized"): return
        self._initialized = True

    @staticmethod
    def get_db_url():
        return URL.create(
            "postgresql+psycopg",
            username=POSTGRES_USER,
            password=POSTGRES_PASSWORD,
            host=POSTGRES_HOST,
            port=POSTGRES_PORT,
            database=POSTGRES_DB,
        )

    @classmethod
    def _get_session(cls):
        if cls._session_factory is None:
            cls._engine = create_engine(
                cls.get_db_url(),
                pool_pre_ping=True,
            )
            cls._session_factory = sessionmaker(
                bind=cls._engine,
                autoflush=False,
                autocommit=False,
            )
        return cls._session_factory()

    @staticmethod
    def _instance(
            session,
            model: Type[Any],
            data: dict[str, Any],
            key: str
    ):
        instance = session.scalar(
            select(model).where(
                getattr(model, key) == data[key]
            )
        )
        if instance is None:
            instance = model(**data)
            session.add(instance)
        else:
            for field, value in data.items():
                setattr(instance, field, value)
        return instance

    @staticmethod
    def save(
            model: Type[Any],
            data: dict[str, Any],
            key: str
    ) -> Any:
        if key not in data:
            raise ValueError(
                f"Key '{key}' not found in data for model '{model.__name__}'"
            )
        session = Db._get_session()
        try:
            instance = Db._instance(
                session,
                model,
                data,
                key
            )
            session.commit()
            session.refresh(instance)
            return instance
        except Exception as e:
            session.rollback()
            raise
        finally:
            session.close()

    @staticmethod
    def save_many(
            records: list[dict[str, Any]],
    ) -> list[Any]:
        session = Db._get_session()
        result = []
        try:
            for record in records:
                model = record['model']
                data = record['data']
                key = record['key']
                if key not in data:
                    raise ValueError(
                        f"Key '{key}' not found in data for model '{model.__name__}'"
                    )
                instance = Db._instance(
                    session,
                    model,
                    data,
                    key
                )
                result.append(instance)
            session.commit()
            for instance in result:
                session.refresh(instance)
            return result
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()
