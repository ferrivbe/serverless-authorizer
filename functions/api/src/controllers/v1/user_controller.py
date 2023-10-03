from fastapi import APIRouter

from models.http_error import HTTPErrorDto
from models.user import UserAdd, UserConfirm, UserCreated
from services.user_service import UserService

router = APIRouter()
service = UserService()


@router.post(
    "",
    tags=["User"],
    status_code=201,
    responses={
        201: {"model": UserCreated},
        404: {"model": HTTPErrorDto},
        422: {"model": HTTPErrorDto},
        500: {"model": HTTPErrorDto},
    },
    response_model=UserCreated,
    response_model_exclude_none=True,
)
async def creates_a_user(user: UserAdd):
    """
    Creates a new user.
    """
    return service.create_user(
        user=user,
    )


@router.patch(
    "/confirm",
    tags=["User"],
    status_code=200,
    responses={
        404: {"model": HTTPErrorDto},
        422: {"model": HTTPErrorDto},
        500: {"model": HTTPErrorDto},
    },
)
async def confirms_a_user(user: UserConfirm):
    """
    Confirms a user.
    """
    return service.confirm_user(
        user_confirm=user,
    )
