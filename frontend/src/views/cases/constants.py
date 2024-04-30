import json
from enum import Enum

from pydantic import TypeAdapter

from src.utils import assets
from src.views.cases.schemas import (
    CaseScheme,
    SkinScheme,
    GoldGroupScheme,
)


SKINS_TYPE = TypeAdapter(dict[str, SkinScheme])
SKINS = SKINS_TYPE.validate_json(open(assets("data/skins.json")).read())

GOLD_GROUPS_TYPE = TypeAdapter(list[GoldGroupScheme])
GOLD_GROUPS = GOLD_GROUPS_TYPE.validate_json(
    open(assets("data/gold_groups.json")).read()
)

CASES_TYPE = TypeAdapter(dict[str, CaseScheme])
CASES = CASES_TYPE.validate_json(open(assets("data/cases.json")).read())

CASE_CUM_WEIGHTS = [2, 7, 32, 157, 782]


class SKIN_GRID_CONF:
    SPACING = 15
    WIDTH = 500
    runs_count = 5  # Количество элементов в строке


class ITEM_CONF:
    HEIGHT_DESC = 30
    WIDTH = (
        SKIN_GRID_CONF.WIDTH
        - SKIN_GRID_CONF.SPACING * (SKIN_GRID_CONF.runs_count - 1)
    ) / SKIN_GRID_CONF.runs_count
    HEIGHT = WIDTH / 4 * 3


class WHEEL_ITEM_CONF:
    WIDTH = 100
    HEIGHT = WIDTH / 4 * 3


WHEEL_ANIMATION_TIME = 6000


class RARITY_COLOR(Enum):
    GOLD = "#e4ae39"
    ANCIENT = "#eb4b4b"
    LEGENDARY = "#d32ce6"
    MYTHICAL = "#8847ff"
    RARE = "#4b69ff"
