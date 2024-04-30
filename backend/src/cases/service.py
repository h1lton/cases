import random

from src.cases.constants import CASE_CUM_WEIGHTS, GOLD_GROUPS
from src.cases.schemas import CaseScheme


def open_case(case: CaseScheme) -> tuple[str, bool]:
    skins_by_rarity: int | list[str] = random.choices(
        [
            case.gold_group,
            case.ancient,
            case.legendary,
            case.mythical,
            case.rare,
        ],
        cum_weights=CASE_CUM_WEIGHTS,
    )[0]

    is_gold = False
    if isinstance(skins_by_rarity, int):
        is_gold = True
        skins_by_rarity = GOLD_GROUPS[skins_by_rarity]

    return random.choice(skins_by_rarity), is_gold
