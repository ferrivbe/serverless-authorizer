import os

from common.constants.environment_variables import EnvironmentVariables
from common.exception.http_error import HTTPInternalServerError


class EnvironmentRepository:
    """
    Handles all interactions with environment variables.
    """

    def __init__(self):
        """
        Initializes a new instance of :class:`EnvironmentRepository` class.
        """
        self.environemnt = os.environ

    def get_cognito_client_id(self):
        """
        Retrieves the value of client identifier environment variable.

        :returns: The value of the environment variable.
        :rtype: str
        """

        return self._get_environment_variable(EnvironmentVariables.CLIENT_ID)

    def get_cognito_client_secret(self):
        """
        Retrieves the value of client secret environment variable.

        :returns: The value of the environment variable.
        :rtype: str
        """

        return self._get_environment_variable(EnvironmentVariables.CLIENT_SECRET)

    def get_region(self):
        """
        Retrieves the value of region environment variable.

        :returns: The value of the environment variable.
        :rtype: str
        """

        return self._get_environment_variable(EnvironmentVariables.REGION)

    def get_userpool_id(self):
        """
        Retrieves the value of userpool identifier environment variable.

        :returns: The value of the environment variable.
        :rtype: str
        """

        return self._get_environment_variable(EnvironmentVariables.USERPOOL_ID)

    def _validate_environment_variable(
        self,
        environment_variable: str,
        environment_variable_name: str,
    ):
        """
        Validates if an environment variable is not None.

        :param str environment_variable: The environment variable to validate.
        :param str environment_variable_name: The name of the environment variable.
        :raises HttpInternalServerError: When the environment variable is None.
        """
        if environment_variable is None:
            raise HTTPInternalServerError(
                "EnvironmentVariableMissing",
                "The environment variable '%(name)s' is missing in current context."
                % {"name": environment_variable_name},
            )

    def _get_environment_variable(self, environment_variable_name: str):
        """
        Retrieves the value of an environment variable.

        :param str environment_variable_name: The name of the environment variable.
        :returns: The value of the environment variable.
        :rtype: str
        :raises HttpInternalServerError: When the environment variable is None.
        """
        environment_variable = os.getenv(environment_variable_name)
        self._validate_environment_variable(
            environment_variable=environment_variable,
            environment_variable_name=environment_variable_name,
        )

        return environment_variable
