from pydantic import BaseModel


class SkinScheme(BaseModel):
    name: str
    rarity: str
    image: str


class GoldGroupScheme(BaseModel):
    name: str
    image: str


class CaseDropScheme(BaseModel):
    gold_group: int
    ancient: list[str]
    legendary: list[str]
    mythical: list[str]
    rare: list[str]


class CaseScheme(BaseModel):
    id: str
    name: str
    image: str
    drop: CaseDropScheme


class WonSkinScheme(BaseModel):
    skin_id: str
    is_gold: bool = False


# FIXME: можно image хранить по id т.к. оно уникально,
#  тем самым убрать это поле и сэкономить память
