from typing import Literal
import sentry_sdk
from app.config import ( SENTRY_DSN, SENTRY_ENVIRONMENT, SENTRY_TRACES_SAMPLE_RATE)
from datetime import datetime

class Sentry:
    _initialized = False

    @staticmethod
    def __init(cls):
        if cls._initialized: return
        Sentry.init_manual()
        cls._initialized = True

    @staticmethod
    def init_manual():
        sentry_sdk.init(
            dsn=SENTRY_DSN,
            environment=SENTRY_ENVIRONMENT,
            traces_sample_rate=SENTRY_TRACES_SAMPLE_RATE,
            enable_logs=True
        )
        run_date = datetime.now().strftime("%Y-%m-%d")
        sentry_sdk.set_tag("run_date", run_date)

    @staticmethod
    def warning(cls, message: str, context: dict | None = None, tags: dict | None = None):
        cls.__init()
        cls._capture(
            message= message,
            level= "warning",
            context= context,
            tags= tags
        )

    @staticmethod
    def error(cls, message: str, context: dict | None = None, tags: dict | None = None):
        cls.__init()
        cls._capture(
            message=message,
            level="error",
            context=context,
            tags=tags
        )

    @staticmethod
    def _capture(
            message: str,
            level: Literal["fatal", "critical", "error", "warning", "info", "debug"] | None,
            context: dict | None = None,
            tags: dict | None = None
    ):
        with sentry_sdk.push_scope() as scope:
            if context:
                for key, value in context.items():
                    scope.set_context(key, value)
            if tags:
                for key, value in tags.items():
                    scope.set_tag(key, value)
            sentry_sdk.capture_message(
                message,
                level= level,
            )