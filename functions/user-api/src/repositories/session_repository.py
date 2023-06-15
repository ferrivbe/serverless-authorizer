from repositories.extensions.generic import GenericExtensions


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

    def refresh_session(self, refresh_token: str):
        """
        Refreshes a user's session using a refresh token.

        :param refresh_token: The refresh token to use for session refresh.
        :type refresh_token: str
        :return: The response object containing the refreshed session details.
        :rtype: object
        """

        import base64
        import json

        # Extract the payload from the refresh token
        payload = refresh_token.split(".")[1]

        # Decode the Base64-encoded payload
        decoded_payload = base64.b64decode(payload + "===").decode("utf-8")

        # Parse the payload as JSON
        payload_json = json.loads(decoded_payload)

        # Extract the Cognito username from the payload
        username = payload_json["username"]

        print("test: " + username)

        return self.cognito_client.initiate_auth(
            ClientId=self.client_id,
            AuthFlow="REFRESH_TOKEN_AUTH",
            AuthParameters={
                "REFRESH_TOKEN": refresh_token,
                "SECRET_HASH": GenericExtensions.get_secret_hash(
                    "36a18771-da22-4a14-9705-6a66143e0688",
                    self.client_id,
                    self.client_secret,
                ),
            },
        )
