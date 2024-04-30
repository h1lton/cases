from fastapi import APIRouter, Depends, HTTPException

from src.cases import service
from src.cases.dependencies import get_case_by_id
from src.cases.schemas import CaseScheme, OpenCaseResponse
from src.logger import logger, extra

router = APIRouter(prefix="/{case_id}")


@router.get("/open", response_model_exclude_defaults=True)
def open_case(
    case_id: str, case: CaseScheme = Depends(get_case_by_id)
) -> OpenCaseResponse:
    if not case:
        raise HTTPException(status_code=404, detail="Case not found")

    skin_id, is_gold = service.open_case(case)

    response = OpenCaseResponse(skin_id=skin_id, is_gold=is_gold)

    logger.info(f"opened case {case_id}" + extra(response))
    return response
