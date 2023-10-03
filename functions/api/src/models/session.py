from enum import Enum

from common.constants.service_constants import ServiceConstants
from pydantic import BaseModel, constr, root_validator


class SessionTargetMethodType(str, Enum):
    POST = "POST"
    GET = "GET"
    PUT = "PUT"
    PATCH = "PATCH"
    DELETE = "DELETE"


class SessionGrantType(str, Enum):
    CLIENT_CREDENTIALS = "client_credentials"
    REFRESH_TOKEN = "refresh_token"


class SessionCreate(BaseModel):
    """
    The session create data transfer object.
    """

    email: str = None
    password: constr(
        regex=r"""^(?!\s+)(?!.*\s+$)(?=.*[A-Z])(?=.*[a-z])(?=.*[0-9])(?=.*[$^*.[\]{}()?"!@#%&/\\,><':;|_~`=+\- ])[A-Za-z0-9$^*.[\]{}()?"!@#%&/\\,><':;|_~`=+\- ]{8,256}$""",
    ) = None
    refresh_token: str = None
    id_token: str = None
    grant_type: SessionGrantType

    @root_validator
    def validate_grant_type(cls, values):
        grant_type = values.get("grant_type")
        email = values.get("email")
        password = values.get("password")
        refresh_token = values.get("refresh_token")
        id_token = values.get("id_token")

        if grant_type == SessionGrantType.CLIENT_CREDENTIALS and (
            not email or not password
        ):
            raise ValueError(
                "Email and password are required for grant type 'client_credentials'"
            )

        if grant_type == SessionGrantType.REFRESH_TOKEN and (
            not refresh_token and not id_token
        ):
            raise ValueError(
                "Refresh token and ID token are required for grant type 'refresh_token'"
            )

        return values


class SessionCreated(BaseModel):
    """
    The session created data transfer object.
    """

    access_token: str
    token_type: str
    expires_in: str
    refresh_token: str = None
    id_token: str = None


class SessionValidate(BaseModel):
    """
    The session to validate.
    """

    access_token: str
    endpoint: str = ServiceConstants.WILDCARD


class SessionValidated(BaseModel):
    """
    The session validated.
    """

    user_id: str
