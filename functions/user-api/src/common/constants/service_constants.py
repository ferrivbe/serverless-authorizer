class ServiceConstants:
    """A class to store constants used in a service."""

    ACCESS_TOKEN = "AccessToken"
    """
    str: The access token.
    """

    AUTHENTICATION_RESULT = "AuthenticationResult"
    """
    str: The authentication result.
    """

    BEARER_PREFIX = "Bearer "
    """
    str: The Bearer prefix.
    """

    CODE = "code"
    """
    str: The code.
    """

    COGNITO_IDP_HANDLER = "cognito-idp"
    """
    str: The cognito IDP handler name.
    """

    CREDENTIALS_DO_NOT_MATCH_MESSAGE = (
        "The credentials do not match any authorized user."
    )
    """
    str: The credentials do not match message.
    """

    DYNAMO_DB_CLIENT_NAME = "dynamodb"
    """
    str: The DynamoDB client name.
    """

    EMAIL = "email"
    """
    str: The email.
    """

    EMPTY_STRING = ""
    """
    str: The empty string.
    """

    EXPIRES_IN = "ExpiresIn"
    """
    str: The expires in.
    """

    INVALID_CODE_MESSAGE = "The code '%(code)s' is invalid, is it the latest?."
    """
    str: The invalid code message.
    """

    INVALID_PASSWORD_MESSAGE = "The password provided is invalid"
    """
    str: The invalid password message.
    """

    REFRESH_TOKEN = "RefreshToken"
    """
    str: The refresh token.
    """

    TOKEN_TYPE = "TokenType"
    """
    str: The token type.
    """

    UNAUTHORIZED_TO_PERFORM_ACTION_MESSAGE = (
        "You are not authorized to perform this action."
    )
    """
    str: The unauthorized to perform action message.
    """

    USER = "user"
    """
    str: The user.
    """

    USER_ALREADY_EXISTS_MESSAGE = "The user with email '%(email)s' already exists."
    """
    str: The message to display when a user already exists.
    """

    USER_BY_USERNAME_ALREADY_EXISTS_MESSAGE = (
        "The user with username '%(username)s' already exists."
    )
    """
    str: The message to display when a user by username already exists.
    """

    USER_CONFIRMED_MESSAGE = "User confirmed, this is where the fun begins!"
    """
    str: The user confirmed message.
    """

    USER_CREATED_EXPECT_VALIDATION_CODE_MESSAGE = (
        "Please confirm your signup, check Email for validation code."
    )
    """
    str: The user created expect validation code message.
    """

    USER_DOES_NOT_EXISTS_MESSAGE = "The user with email '%(email)s' does not exist."
    """
    str: The user does not exist message.
    """

    USER_NOT_CONFIRMED_MESSAGE = (
        "The user '%(email)s' is not confirmed in our system, check your email."
    )
    """
    The user not confirmed message.
    """

    USERNAME = "username"
    """
    str: The username.
    """

    VALUE_ERROR = "ValueError"
    """
    Error code for a value error.
    """

    WILDCARD = "/"
    """
    str: Wildcard character used in certain contexts.

    This constant represents a wildcard character ("/") that is used in specific contexts within the codebase.
    """

    ZERO_ITEMS = 0
    """
    int: The zero items validation.
    """
