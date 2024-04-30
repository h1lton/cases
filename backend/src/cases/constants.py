import json

from pydantic import TypeAdapter

from src.cases.schemas import CaseScheme

CASE_CUM_WEIGHTS = [2, 7, 32, 157, 782]
# Алгоритм получения case_cum_weights
# class CaseWeights(IntEnum):
#     gold = 2
#     ancient = 5
#     legendary = 5 * ancient
#     mythical = 5 * legendary
#     rare = 5 * mythical
#
# case_rarities = []
# case_weights = []
#
# for item in list(CaseWeights):
#     rarities.append(item.name)
#     weights.append(item.value)
#
# cum_case_weights = list(itertools.accumulate(weights))

GOLD_GROUPS: list[list[str]] = json.load(open("gold_groups.json"))

CASES_TYPE = TypeAdapter(dict[str, CaseScheme])
CASES = CASES_TYPE.validate_json(open("cases.json").read())
