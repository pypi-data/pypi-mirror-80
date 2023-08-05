import structlog
import logging
import sys
import os

from structlog import wrap_logger
from structlog.processors import JSONRenderer
from structlog.stdlib import filter_by_level
from structlog.stdlib import add_log_level_number


def rename_message_key(_, __, event_dict):
    event_dict["message"] = event_dict["event"]
    event_dict.pop("event", None)
    return event_dict


def increase_level_numbers(_, __, event_dict):
    event_dict["level"] = event_dict["level_number"] * 10
    event_dict.pop("level_number", None)
    return event_dict


level = os.getenv("LOG_LEVEL", "INFO")

logging.basicConfig(stream=sys.stdout, format="%(message)s", level=level)
bufflog = wrap_logger(
    logging.getLogger(__name__),
    processors=[
        filter_by_level,
        rename_message_key,
        add_log_level_number,
        increase_level_numbers,
        JSONRenderer(),
    ],
)
