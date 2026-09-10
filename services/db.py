from datetime import datetime
from sqlalchemy import create_engine, select, func
from sqlalchemy.engine import URL
from sqlalchemy.orm import sessionmaker
from app.config import (
    POSTGRES_HOST,POSTGRES_PORT,POSTGRES_USER,POSTGRES_PASSWORD,POSTGRES_DB
)
from typing import Any, Type
from exceptions.minio import MinioException

class Query:
    def __init__(self, model: Type[Any]):
        self.model = model
        self._query = select(model)

    def select(self, fields: list[str]):
        columns = [
            getattr(self.model, field)
            for field in fields
        ]
        self._query = select(*columns)
        return self

    def where(
        self,
        field: str,
        operator: str,
        value: Any,
    ):
        column = getattr(self.model, field)
        if operator == "=": condition = column == value
        if operator == "!=": condition = column != value
        if operator == ">": condition = column > value
        if operator == "<": condition = column < value
        if operator == ">=": condition = column >= value
        if operator == "<=": condition = column <= value
        if operator.lower() == "like": condition = column.like(value)
        if operator.lower() == "ilike": condition = column.ilike(value)
        if operator.lower() == "in": condition = column.in_(value)
        try:
            self._query = self._query.where(condition)
            return self
        except ValueError:
            raise ValueError(f"Unsupported operator: {operator}")
        except Exception as e:
            raise MinioException(e) from e

    def where_date(self, field: str, value: Any):
        column = getattr(self.model, field)
        if isinstance(value, str):
            value = datetime.strptime(value, "%Y-%m-%d").date()
        try:
            self._query = self._query.where(func.date(column) == value)
            return self
        except Exception as e:
            raise MinioException(e) from e

    def get(self):
        session = Db._get_session()
        try:
            result = session.execute(self._query)
            return result.all()
        finally:
            session.close()

    def first(self):
        session = Db._get_session()
        try:
            result = session.execute(self._query)
            return result.first()
        finally:
            session.close()

    def count(self):
        count_query = select(
            func.count()
        ).select_from(
            self._query.subquery()
        )
        session = Db._get_session()
        try:
            return session.scalar(count_query)
        finally:
            session.close()

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
    def query(model: Type[Any]) -> Query:
        return Query(model)

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
            model: Type[Any],
            records: list[dict[str, Any]],
            key: str
    ) -> list[Any]:
        session = Db._get_session()
        result = []
        try:
            for data in records:
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
