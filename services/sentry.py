from typing import Literal
import sentry_sdk
from app.config import ( SENTRY_DSN, SENTRY_ENVIRONMENT, SENTRY_TRACES_SAMPLE_RATE)
from datetime import datetime

class Sentry:
    _initialized = False

    @classmethod
    def init(cls):
        if cls._initialized: return
        sentry_sdk.init(
            dsn=SENTRY_DSN,
            environment=SENTRY_ENVIRONMENT,
            traces_sample_rate=SENTRY_TRACES_SAMPLE_RATE,
            enable_logs=True
        )
        run_date = datetime.now().strftime("%Y-%m-%d")
        sentry_sdk.set_tag("run_date", run_date)
        cls._initialized = True

    @classmethod
    def warning(
            cls,
            message: str,
            context: dict | None = None,
            tags: dict | None = None,
            extra: dict | None = None
    ):
        cls.init()
        cls._capture(
            message= message,
            level= "warning",
            context= context,
            tags= tags,
            extra= extra
        )

    @classmethod
    def error(
            cls,
            message: str,
            context: dict | None = None,
            tags: dict | None = None,
            extra: dict | None = None
    ):
        cls.init()
        cls._capture(
            message= message,
            level= "error",
            context= context,
            tags= tags,
            extra= extra
        )

    @staticmethod
    def _capture(
            message: str,
            level: Literal["fatal", "critical", "error", "warning", "info", "debug"] | None,
            context: dict | None = None,
            tags: dict | None = None,
            extra: dict | None = None,
    ):
        with sentry_sdk.push_scope() as scope:
            if context:
                for key, value in context.items():
                    scope.set_context(key, value)
            if tags:
                for key, value in tags.items():
                    scope.set_tag(key, value)
            if extra:
                for key, value in extra.items():
                    scope.set_extra(key, value)
            sentry_sdk.capture_message(
                message,
                level= level,
            )