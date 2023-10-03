from datetime import datetime

import boto3
from common.constants.service_constants import ServiceConstants
from repositories.extensions.generic import GenericExtensions


class UserRepository:
    """
    This class manages user operations in the Cognito user pool.

    :param client_id: The client ID of the Cognito user pool.
    :type client_id: str
    :param client_secret: The client secret of the Cognito user pool.
    :type client_secret: str
    :param client: The Cognito client.
    :type client: boto3.client
    """

    def __init__(self, client_id: str, client_secret: str, client: any):
        """
        Initializes a new instance of the UserRepository class.
        """
        self.client_id = client_id
        self.client_secret = client_secret
        self.cognito_client = client

        dynamodb_client = boto3.resource(ServiceConstants.DYNAMO_DB_CLIENT_NAME)
        self.user_table = dynamodb_client.Table(ServiceConstants.USER)

    def create_user(self, email: str, username: str, password: str):
        """
        Creates a new user in the Cognito user pool.

        :param email: The email of the user to create.
        :type email: str
        :param username: The username of the user to create.
        :type username: str
        :param password: The password of the user to create.
        :type password: str
        :return: The response object containing the details of the created user.
        """
        response = self.cognito_client.sign_up(
            ClientId=self.client_id,
            SecretHash=GenericExtensions.get_secret_hash(
                email,
                self.client_id,
                self.client_secret,
            ),
            Username=email,
            Password=password,
            UserAttributes=[
                {"Name": "email", "Value": email},
            ],
            ValidationData=[
                {"Name": "email", "Value": email},
            ],
        )

        user_item = {
            "id": response["UserSub"],
            "email": email,
            "username": username,
            "role": "end_user",
            "confirmed": False,
            "created_at": datetime.utcnow().isoformat(),
        }

        self.user_table.put_item(Item=user_item)

        return response

    def confirm_user(self, email: str, code: str) -> str:
        """
        Confirms a user with the given email and confirmation code.

        :param email: The email of the user to confirm.
        :type email: str
        :param code: The confirmation code.
        :type code: str
        :return: The username of the confirmed user.
        :rtype: str
        """
        self.cognito_client.confirm_sign_up(
            ClientId=self.client_id,
            SecretHash=GenericExtensions.get_secret_hash(
                email,
                self.client_id,
                self.client_secret,
            ),
            Username=email,
            ConfirmationCode=code,
            ForceAliasCreation=False,
        )

        items = self.get_user_by_email(email=email)
        self.user_table.update_item(
            Key={"id": items[0]["id"]},
            UpdateExpression="SET confirmed = :val, confirmed_at = :timeval",
            ExpressionAttributeValues={
                ":val": True,
                ":timeval": datetime.utcnow().isoformat(),
            },
        )

        return items[0]["username"]

    def get_user_by_email(self, email: str) -> list:
        """
        Retrieves a user by their email.

        :param email: The email of the user to retrieve.
        :type email: str
        :return: A list of items matching the email.
        :rtype: list
        """
        response = self.user_table.scan(
            FilterExpression="email = :val",
            ExpressionAttributeValues={":val": email},
        )

        return response["Items"]

    def get_user_by_username(self, username: str) -> list:
        """
        Retrieves a user by their username.

        :param username: The username of the user to retrieve.
        :type username: str
        :return: A list of items matching the username.
        :rtype: list
        """
        response = self.user_table.scan(
            FilterExpression="username = :val",
            ExpressionAttributeValues={":val": username},
        )

        return response["Items"]

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
