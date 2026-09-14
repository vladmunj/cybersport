import argparse
import importlib
import traceback
from services.logger import Logger
from services.sentry import Sentry

def run_pipeline(pipeline_name: str) -> None:
    __logger = Logger()
    parts = pipeline_name.split(".")
    if len(parts) < 2:
        raise ValueError(
            "Pipeline must have at least two parts. "
            "Example: clickhouse.mart_player_performance"
        )
    module_name = (
        f"app.pipeline.{pipeline_name}.pipeline"
    )
    pipeline_name_only = parts[-1]
    function_name = (
        f"run_{pipeline_name_only}_pipeline"
    )
    try:
        module = importlib.import_module(module_name)
        pipeline = getattr(module, function_name)
    except (ModuleNotFoundError, AttributeError) as exception:
        __logger.error(
            f"Failed to load pipeline "
            f"{pipeline_name}: {exception}"
        )
        Sentry.error(
            message= (
                f"Failed to load pipeline: "
                f"{pipeline_name}"
            ),
            exception= exception,
            extra= {
                "pipeline": pipeline_name,
                "module": module_name,
                "function": function_name,
                "traceback": traceback.format_exc(),
            },
        )
        raise
    __logger.info(f"Starting pipeline: {pipeline_name}")
    try:
        pipeline()
        __logger.info(
            f"Pipeline completed successfully: "
            f"{pipeline_name}"
        )
    except Exception as exception:
        __logger.error(
            f"Pipeline failed "
            f"{pipeline_name}: {exception}"
        )
        Sentry.error(
            message=(
                f"Pipeline failed: "
                f"{pipeline_name}"
            ),
            exception=exception,
            extra={
                "pipeline": pipeline_name,
                "traceback": traceback.format_exc(),
            },
        )
        raise

def main():
    parser = argparse.ArgumentParser(description="Run data pipeline")
    parser.add_argument(
        "pipeline",
        help=(
            "Pipeline name. "
            "Example: clickhouse.mart_player_performance"
        ),
    )
    args = parser.parse_args()
    run_pipeline(args.pipeline)

if __name__ == "__main__": main()