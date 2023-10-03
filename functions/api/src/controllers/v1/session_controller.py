from fastapi import APIRouter
from models.http_error import HTTPErrorDto
from models.session import (
    SessionCreate,
    SessionCreated,
    SessionValidate,
    SessionValidated,
)
from services.session_service import SessionService

router = APIRouter()
service = SessionService()


@router.post(
    "",
    tags=["Session"],
    status_code=200,
    responses={
        200: {"model": SessionCreated},
        404: {"model": HTTPErrorDto},
        422: {"model": HTTPErrorDto},
        500: {"model": HTTPErrorDto},
    },
    response_model=SessionCreated,
    response_model_exclude_none=True,
)
async def creates_a_new_session(user: SessionCreate):
    """
    Creates a new session.
    """
    return service.login_user(
        user=user,
    )


@router.post(
    "/validate",
    tags=["Session"],
    status_code=200,
    responses={
        200: {"model": SessionValidated},
        404: {"model": HTTPErrorDto},
        422: {"model": HTTPErrorDto},
        500: {"model": HTTPErrorDto},
    },
    response_model=SessionValidated,
    response_model_exclude_none=True,
)
async def validates_the_session(session: SessionValidate):
    """
    Validates the user session token and data.
    """
    user_id = service.validate_session_token(session.access_token)

    return SessionValidated(
        user_id=user_id,
    )
