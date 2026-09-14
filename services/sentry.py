import sentry_sdk

class Sentry:
    @staticmethod
    def warning(message):
        sentry_sdk.capture_message(
            message,
            level="warning",
        )

    @staticmethod
    def error(message):
        sentry_sdk.capture_message(
            message,
            level="error",
        )