from pydantic import BaseModel


class CaseScheme(BaseModel):
    gold_group: int
    ancient: list[str]
    legendary: list[str]
    mythical: list[str]
    rare: list[str]


class OpenCaseResponse(BaseModel):
    skin_id: str
    is_gold: bool = False
