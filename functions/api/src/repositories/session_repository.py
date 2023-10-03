import requests
from jose import jwk, jwt
from repositories.environment_repository import EnvironmentRepository
from repositories.extensions.generic import GenericExtensions
from common.exception.http_error import HTTPError


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

    def verify_id_token(self, id_token: str) -> dict:
        """
        Verifies the identification token and returns its payload.

        :param id_token: The identification token.
        :type id_token: str
        :return: Verified token payload or None if verification fails.
        """
        header = jwt.get_unverified_header(id_token)
        region = self.environment_repository.get_region()
        user_pool_id = self.environment_repository.get_userpool_id()

        jwks_url = f"https://cognito-idp.{region}.amazonaws.com/{user_pool_id}/.well-known/jwks.json"
        jwks = requests.get(jwks_url).json()

        rsa_key = {}
        for key in jwks["keys"]:
            if key["kid"] == header["kid"]:
                rsa_key = {"kty": key["kty"], "e": key["e"], "n": key["n"]}

        payload = jwt.decode(
            id_token,
            rsa_key,
            algorithms=["RS256"],
            audience=self.client_id,
            issuer=f"https://cognito-idp.{region}.amazonaws.com/{user_pool_id}",
        )
        return payload

    def get_username_from_id_token(self, id_token: str) -> str:
        """
        Gets username from identification token.

        :param id_token: The identification token.
        :type id_token: str
        :return: The username.
        """
        payload = self.verify_id_token(id_token)
        if payload and "cognito:username" in payload:
            return payload["cognito:username"]
        else:
            raise HTTPError(
                404,
                "InvalidIdToken",
                "The id token provided is not valid.",
            )

    def refresh_session(self, refresh_token: str, id_token: str):
        """
        Logs in a user using a refresh token.

        :param refresh_token: The refresh token of the user.
        :type refresh_token: str
        :param id_token: The identification token of the user.
        :type id_token: str
        :return: The response object containing the login details.
        """
        user_id = self.get_username_from_id_token(
            id_token=id_token,
        )

        return self.cognito_client.initiate_auth(
            ClientId=self.client_id,
            AuthFlow="REFRESH_TOKEN_AUTH",
            AuthParameters={
                "REFRESH_TOKEN": refresh_token,
                "SECRET_HASH": GenericExtensions.get_secret_hash(
                    user_id,
                    self.client_id,
                    self.client_secret,
                ),
            },
        )
