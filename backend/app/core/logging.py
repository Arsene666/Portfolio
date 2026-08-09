import logging
import sys


def configure_logging(environment: str = "development") -> None:
    """Configure a simple, structured console logger.

    Kept dependency-free (stdlib only) for Phase 1. Can be swapped for
    loguru or structlog later without touching call sites, since routes
    only ever do `logging.getLogger(__name__)`.
    """
    level = logging.DEBUG if environment == "development" else logging.INFO

    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(
        logging.Formatter(
            fmt="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
            datefmt="%Y-%m-%dT%H:%M:%S",
        )
    )

    root = logging.getLogger()
    root.setLevel(level)
    root.handlers = [handler]
