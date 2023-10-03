from http import HTTPStatus

import boto3
import cognitojwt
from common.constants.error_codes import ErrorCodes
from common.constants.service_constants import ServiceConstants
from common.exception.http_error import HTTPError
from models.session import SessionCreate, SessionCreated, SessionGrantType
from repositories.environment_repository import EnvironmentRepository
from repositories.session_repository import SessionRepository


class SessionService:
    """This class is used to manage session operations in the Cognito user pool.

    :ivar repository: The session repository.
    :vartype repository: SessionRepository
    """

    def __init__(self):
        """
        Initializes a new instance of the SessionService class.
        """
        self.environment_repository = EnvironmentRepository()
        self.client = boto3.client(ServiceConstants.COGNITO_IDP_HANDLER)

        self.repository = SessionRepository(
            client_id=self.environment_repository.get_cognito_client_id(),
            client_secret=self.environment_repository.get_cognito_client_secret(),
            client=self.client,
        )

    def login_user(self, user: SessionCreate) -> SessionCreated:
        """
        Logs in a user with the given email and password.

        :param email: The email of the user to log in.
        :type email: str
        :param password: The password of the user.
        :type password: str
        :return: The response object containing the login details.
        """
        try:
            if user.grant_type == SessionGrantType.CLIENT_CREDENTIALS:
                response = self.repository.login_user(
                    email=user.email,
                    password=user.password,
                )
            elif user.grant_type == SessionGrantType.REFRESH_TOKEN:
                response = self.repository.refresh_session(
                    refresh_token=user.refresh_token,
                    id_token=user.id_token,
                )

            return SessionCreated(
                token_type=response[ServiceConstants.AUTHENTICATION_RESULT][
                    ServiceConstants.TOKEN_TYPE
                ],
                access_token=response[ServiceConstants.AUTHENTICATION_RESULT][
                    ServiceConstants.ACCESS_TOKEN
                ],
                expires_in=response[ServiceConstants.AUTHENTICATION_RESULT][
                    ServiceConstants.EXPIRES_IN
                ],
                refresh_token=response[ServiceConstants.AUTHENTICATION_RESULT].get(
                    ServiceConstants.REFRESH_TOKEN
                ),
                id_token=response[ServiceConstants.AUTHENTICATION_RESULT].get(
                    ServiceConstants.ID_TOKEN
                ),
            )

        except self.client.exceptions.NotAuthorizedException:
            raise HTTPError(
                HTTPStatus.UNAUTHORIZED,
                ErrorCodes.UNAUTHORIZED_TO_PERFORM_ACTION,
                ServiceConstants.CREDENTIALS_DO_NOT_MATCH_MESSAGE,
            )

        except self.client.exceptions.UserNotConfirmedException:
            raise HTTPError(
                HTTPStatus.UNPROCESSABLE_ENTITY,
                ErrorCodes.USER_NOT_CONFIRMED,
                ServiceConstants.USER_NOT_CONFIRMED_MESSAGE
                % {ServiceConstants.EMAIL: user.email},
            )

        except self.client.exceptions.UserNotFoundException:
            raise HTTPError(
                HTTPStatus.UNPROCESSABLE_ENTITY,
                ErrorCodes.USER_NOT_FOUND,
                ServiceConstants.USER_DOES_NOT_EXISTS_MESSAGE
                % {ServiceConstants.EMAIL: user.email},
            )

    def validate_session_token(self, token: str):
        """
        Validates the session token.

        :param token: The user token to be validated.
        """
        token = token.replace(
            ServiceConstants.BEARER_PREFIX,
            ServiceConstants.EMPTY_STRING,
        )
        try:
            verified_claims: dict = cognitojwt.decode(
                token,
                self.environment_repository.get_region(),
                self.environment_repository.get_userpool_id(),
                app_client_id=self.environment_repository.get_cognito_client_id(),
                testmode=False,
            )

            return verified_claims.get("username")
        except Exception as exception:
            print(exception)
            raise HTTPError(
                HTTPStatus.UNAUTHORIZED,
                "UserUnauthorized",
                "This user is not authorized, provide a valid and not expired token.",
            )
