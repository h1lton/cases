from src.cases.constants import CASES


def get_case_by_id(case_id: str):
    return CASES.get(case_id)
