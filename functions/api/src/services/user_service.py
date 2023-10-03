from http import HTTPStatus

import boto3
from common.constants.error_codes import ErrorCodes
from common.constants.service_constants import ServiceConstants
from common.exception.http_error import HTTPError
from models.user import UserAdd, UserConfirm, UserCreated
from repositories.environment_repository import EnvironmentRepository
from repositories.user_repository import UserRepository


class UserService:
    """This class is used to manage user operations in the Cognito user pool.

    :ivar repository: The user repository.
    :vartype repository: UserRepository
    """

    def __init__(self):
        """
        Initializes a new instance of the UserService class.
        """
        self.environment_repository = EnvironmentRepository()
        self.client = boto3.client(ServiceConstants.COGNITO_IDP_HANDLER)

        self.repository = UserRepository(
            client_id=self.environment_repository.get_cognito_client_id(),
            client_secret=self.environment_repository.get_cognito_client_secret(),
            client=self.client,
        )

    def create_user(self, user: UserAdd) -> UserCreated:
        """Creates a new user in the Cognito user pool with the given email and password.

        :param email: The email of the user to create.
        :type email: str
        :param password: The password of the user to create.
        :type password: str
        :return: The response object containing the details of the created user.
        """
        users = self.repository.get_user_by_username(user.username)
        self._validate_users(users=users, username=user.username)

        try:
            self.repository.create_user(
                email=user.email,
                username=user.username,
                password=user.password,
            )

            return UserCreated(
                email=user.email,
                username=user.username,
                message=ServiceConstants.USER_CREATED_EXPECT_VALIDATION_CODE_MESSAGE,
            )

        except self.client.exceptions.UsernameExistsException:
            raise HTTPError(
                HTTPStatus.UNPROCESSABLE_ENTITY,
                ErrorCodes.USER_ALREADY_EXISTS,
                ServiceConstants.USER_ALREADY_EXISTS_MESSAGE
                % {ServiceConstants.EMAIL: user.email},
            )

        except self.client.exceptions.InvalidPasswordException:
            raise HTTPError(
                HTTPStatus.BAD_REQUEST,
                ErrorCodes.NOT_VALID_PASSWORD,
                ServiceConstants.INVALID_PASSWORD_MESSAGE,
            )

        except self.client.exceptions.UserLambdaValidationException:
            raise HTTPError(
                HTTPStatus.UNPROCESSABLE_ENTITY,
                ErrorCodes.USER_ALREADY_EXISTS,
                ServiceConstants.USER_ALREADY_EXISTS_MESSAGE
                % {ServiceConstants.EMAIL: user.email},
            )

        except Exception as exception:
            raise HTTPError(
                500,
                ErrorCodes.INTERNAL_SERVER_ERROR,
                str(exception),
            )

    def confirm_user(self, user_confirm: UserConfirm) -> UserCreated:
        """Confirms an existing user with the given email and confirmation code.

        :param email: The email of the user to confirm.
        :type email: str
        :param code: The confirmation code.
        :type code: str
        :return: The response object containing the confirmation details.
        """
        try:
            username = self.repository.confirm_user(
                email=user_confirm.email,
                code=user_confirm.code,
            )

            return UserCreated(
                email=user_confirm.email,
                username=username,
                message=ServiceConstants.USER_CONFIRMED_MESSAGE,
            )

        except self.client.exceptions.UserNotFoundException:
            raise HTTPError(
                HTTPStatus.NOT_FOUND,
                ErrorCodes.USER_NOT_FOUND,
                ServiceConstants.USER_DOES_NOT_EXISTS_MESSAGE
                % {ServiceConstants.EMAIL: user_confirm.email},
            )

        except self.client.exceptions.CodeMismatchException:
            raise HTTPError(
                HTTPStatus.UNPROCESSABLE_ENTITY,
                ErrorCodes.INVALID_CONFIRMATION_CODE,
                ServiceConstants.INVALID_CODE_MESSAGE
                % {ServiceConstants.CODE: user_confirm.code},
            )

        except self.client.exceptions.NotAuthorizedException:
            raise HTTPError(
                HTTPStatus.UNAUTHORIZED,
                ErrorCodes.UNAUTHORIZED_TO_PERFORM_ACTION,
                ServiceConstants.UNAUTHORIZED_TO_PERFORM_ACTION_MESSAGE,
            )

        except Exception as exception:
            raise HTTPError(
                HTTPStatus.INTERNAL_SERVER_ERROR,
                ErrorCodes.INTERNAL_SERVER_ERROR,
                str(exception),
            ) from exception

    def _validate_users(self, users: list, username: str):
        """
        Validates a list of users to ensure that the given username does not already exist.

        :param users: The list of users to validate.
        :type users: list
        :param username: The username to check for existence.
        :type username: str
        :raises HTTPError: If the username already exists in the list of users.
        """
        if len(users) > ServiceConstants.ZERO_ITEMS:
            raise HTTPError(
                HTTPStatus.UNPROCESSABLE_ENTITY,
                ErrorCodes.USER_ALREADY_EXISTS,
                ServiceConstants.USER_BY_USERNAME_ALREADY_EXISTS_MESSAGE
                % {ServiceConstants.USERNAME: username},
            )
