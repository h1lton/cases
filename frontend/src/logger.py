import json
import sys

from loguru import logger as _logger
from pydantic import BaseModel

_logger.level("INFO", color="<b><lw>")
_logger.level("CRITICAL", color="<b><lw><bg red>")

logger = _logger.opt(colors=True)

logger.remove()
logger.add(
    sys.stdout,
    format="<lm>[<lg>{time:HH:mm:ss}</>]"
    " <lvl>{level}</> | "
    "<b><c>{name}</></>:<b><c>{function}</></>:<b><c>{line}</></>"
    " - <lvl>{message}</lvl></>",
    level="INFO",
    colorize=True,
)

# FIXME: в определенных сценариях нету цветного вывода


def extra(data: dict | list | str | BaseModel) -> str:
    s = ""
    if isinstance(data, (dict, list)):
        s = json.dumps(data, indent=4)
    elif isinstance(data, str):
        s = data
    elif isinstance(data, BaseModel):
        s = data.model_dump_json(indent=4)
    return f"\n<white>{s}</>"
