from repositories.extensions.generic import GenericExtensions
from repositories.environment_repository import EnvironmentRepository


class SessionRepository:
    """
    This class manages session operations in the Cognito user pool.

    :param client_id: The client ID of the Cognito user pool.
    :type client_id: str
    :param client_secret: The client secret of the Cognito user pool.
    :type client_secret: str
    :param client: The Cognito client.
    :type client: boto3.client
    """

    def __init__(self, client_id: str, client_secret: str, client: any):
        """
        Initializes a new instance of the SessionRepository class.
        """
        self.client_id = client_id
        self.client_secret = client_secret
        self.cognito_client = client
        self.environment_repository = EnvironmentRepository()

    def login_user(self, email: str, password: str):
        """
        Logs in a user with the given email and password.

        :param email: The email of the user to log in.
        :type email: str
        :param password: The password of the user.
        :type password: str
        :return: The response object containing the login details.
        """
        return self.cognito_client.initiate_auth(
            ClientId=self.client_id,
            AuthFlow="USER_PASSWORD_AUTH",
            AuthParameters={
                "USERNAME": email,
                "PASSWORD": password,
                "SECRET_HASH": GenericExtensions.get_secret_hash(
                    email,
                    self.client_id,
                    self.client_secret,
                ),
            },
        )

    def get_username_from_refresh_token(self, refresh_token):
        response = self.client.list_users(
            UserPoolId=self.environment_repository.get_userpool_id(),
            Filter=f"refresh_token='{refresh_token}'",
        )

        if "Users" in response:
            users = response["Users"]
            if len(users) > 0:
                return users[0]["Username"]

        return None

    def refresh_session(self, refresh_token: str):
        """
        Logs in a user using a refresh token.

        :param refresh_token: The refresh token of the user.
        :type refresh_token: str
        :return: The response object containing the login details.
        """
        user_id = self.get_username_from_refresh_token(
            refresh_token=refresh_token,
        )

        print(user_id)

        return self.cognito_client.initiate_auth(
            ClientId=self.client_id,
            AuthFlow="REFRESH_TOKEN_AUTH",
            AuthParameters={
                "REFRESH_TOKEN": refresh_token,
                "SECRET_HASH": GenericExtensions.get_secret_hash(
                    user_id,  # Assuming you have the username stored
                    self.client_id,
                    self.client_secret,
                ),
            },
        )
