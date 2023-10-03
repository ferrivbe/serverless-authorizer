from fastapi import APIRouter
from models.health import HealthDto
from models.http_error import HTTPErrorDto

router = APIRouter()


@router.get(
    "",
    tags=["Health"],
    status_code=200,
    responses={
        200: {"model": HealthDto},
        500: {"model": HTTPErrorDto},
    },
    response_model=HealthDto,
    response_model_exclude_none=True,
)
async def gets_current_health():
    """
    Gets current health.
    """

    return HealthDto(
        healthy=True,
    )
