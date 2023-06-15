import logging
import logging.config
import sys

from fastapi import Request
from utils.formatter import LoggerJSONFormatter

logging_config = {
    "version": 1,
    "disable_existing_loggers": True,
    "formatters": {
        "json": {
            "()": LoggerJSONFormatter,
            "format": "{levelname} {asctime} {message} {detail}",
            "style": "{",
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "level": "DEBUG",
            "formatter": "json",
            "stream": sys.stderr,
        },
    },
    "loggers": {
        __name__: {
            "handlers": ["console"],
            "level": "DEBUG",
            "propagate": False,
        },
    },
}

logging.config.dictConfig(logging_config)


class LoggerHandler:
    """
    A class for generating log messages for a given HTTP request.

    This class provides a standardized way to generate log messages for an HTTP
    request. It contains methods for logging various levels of messages, as well
    as a method for populating details about the request to be included in the logs.
    """

    def __init__(self, request: Request, service_name: str = "serverless-authorizer"):
        """
        Initializes a new instance of the LoggerHandler class.

        :param request: An object representing the HTTP request to be logged.
        :type request: Request
        :param service_name: The name of the service for which the logs are being generated.
        :type service_name: str
        """
        self.request = request
        self.service_name = service_name

        self._logger = logging.getLogger(__name__)

        self.trim_properties = [
            "file_content",
            "access_token",
            "refresh_token",
        ]

        self.mask_properties = [
            "password",
        ]

    def _format_payload(self, payload: dict) -> dict:
        """
        Formats the payload with masked and trimmed properties.

        :param payload: A dictionary containing the payload of the request.
        :type payload: dict
        :return: A dictionary containing the formatted properties.
        :rtype: dict
        """
        if payload is not None:
            for key in payload:
                if len(payload[key].__str__()) > 100 and key in self.trim_properties:
                    payload[key] = payload[key][:100]

            for key in payload:
                if key in self.mask_properties:
                    payload[key] = "[masked]"

        return payload

    def _get_headers(self) -> dict:
        """
        Gets the headers from an HTTP entity.

        :return: The headers of the HTTP entity as a dictionary.
        :rtype: dict
        """
        return dict(self.request.headers)

    def _populate_detail(self, payload: dict) -> dict:
        """
        Populates the details of the request made to a service.

        :param payload: A dictionary containing the payload of the request.
        :type payload: dict
        :return: A dictionary containing the service name, HTTP method, scheme,
                host, endpoint, payload, x-forwarded-for, and request ID of the request.
        :rtype: dict
        """
        self.request_headers = self._get_headers()

        return {
            "service_name": self.service_name,
            "method": self.request.method,
            "scheme": self.request.scope.get("type"),
            "host": self.request_headers.get("host"),
            "endpoint": self.request.url.path,
            "payload": self._format_payload(payload),
            "x-forwarded-for": self.request_headers.get("x-forwarded-for"),
            "request_id": self.request.state.request_id,
        }

    def info(self, payload: dict, message: str = "event") -> None:
        """
        Logs an informational message with the given payload.

        :param payload: A dictionary containing the payload of the request.
        :type payload: dict
        :param message: A string representing the message to be logged.
        :type message: str
        :return: None
        """
        if self.request.url.path == "/openapi.json":
            return

        self._logger.info(
            msg=message,
            extra={"detail": self._populate_detail(payload)},
        )

    def exception(self, payload: dict, message: str = "event") -> None:
        """
        Logs an exception message with the given payload.

        :param payload: A dictionary containing the payload of the request.
        :type payload: dict
        :param message: A string representing the message to be logged.
        :type message: str
        :return: None
        """
        self._logger.exception(
            msg=message,
            extra={"detail": self._populate_detail(payload)},
        )

    def error(self, payload: dict, message: str = "event") -> None:
        """
        Logs an error message with the given payload.

        :param payload: A dictionary containing the payload of the request.
        :type payload: dict
        :param message: A string representing the message to be logged.
        :type message: str
        :return: None
        """
        self._logger.error(
            msg=message,
            extra={"detail": self._populate_detail(payload)},
        )
