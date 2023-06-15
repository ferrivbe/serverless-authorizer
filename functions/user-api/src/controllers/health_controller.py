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
)
async def gets_current_health():
    """
    Gets current health.
    """

    return HealthDto(
        healthy=True,
    )
