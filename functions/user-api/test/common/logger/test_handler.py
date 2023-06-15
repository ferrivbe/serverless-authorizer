from fastapi import Request
from src.common.logger.handler import LoggerHandler


class TestLoggerHandler:
    def _setup(self):
        self.request = Request(scope={}, headers={}, state={})
        self.logger_handler = LoggerHandler(request=self.request)

    def test_init(self):
        assert self.logger_handler.request == self.request
        assert self.logger_handler.service_name == "serverless-authorizer"

    def test__format_payload_with_trim_properties(self):
        payload = {"file_content": "a" * 200}
        formatted_payload = self.logger_handler._format_payload(payload)
        assert formatted_payload == {"file_content": "a" * 100}

    def test__format_payload_with_mask_properties(self):
        payload = {"password": "secret"}
        self.logger_handler.mask_properties = ["password"]
        formatted_payload = self.logger_handler._format_payload(payload)
        assert formatted_payload == {"password": "[masked]"}

    def test__get_headers(self):
        self.request.headers = {"Content-Type": "application/json"}
        headers = self.logger_handler._get_headers()
        assert headers == {"Content-Type": "application/json"}

    def test__populate_detail(self):
        payload = {"key": "value"}
        self.request.method = "POST"
        self.request.scope = {"type": "http", "headers": {"host": "example.com"}}
        self.request.url.path = "/path"
        self.request.state.request_id = "request_id"
        self.logger_handler.service_name = "service"
        self.logger_handler.trim_properties = ["key"]
        detail = self.logger_handler._populate_detail(payload)
        expected_detail = {
            "service_name": "service",
            "method": "POST",
            "scheme": "http",
            "host": "example.com",
            "endpoint": "/path",
            "payload": {"key": "value"},
            "x-forwarded-for": None,
            "request_id": "request_id",
        }
        assert detail == expected_detail

    def test_info(self, caplog):
        payload = {"key": "value"}
        self.logger_handler.info(payload=payload, message="event")
        expected_extra = {"detail": self.logger_handler._populate_detail(payload)}
        assert "event" in caplog.text
        assert str(expected_extra) in caplog.text

    def test_exception(self, caplog):
        payload = {"key": "value"}
        self.logger_handler.exception(payload=payload, message="event")
        expected_extra = {"detail": self.logger_handler._populate_detail(payload)}
        assert "event" in caplog.text
        assert str(expected_extra) in caplog.text

    def test_error(self, caplog):
        payload = {"key": "value"}
        self.logger_handler.error(payload=payload, message="event")
        expected_extra = {"detail": self.logger_handler._populate_detail(payload)}
        assert "event" in caplog.text
        assert str(expected_extra) in caplog.text

    def test__format_payload_with_trim_and_mask_properties(self):
        payload = {"password": "secret", "file_content": "a" * 200}
        self.logger_handler.mask_properties = ["password"]
        self.logger_handler.trim_properties = ["file_content"]
        formatted_payload = self.logger_handler._format_payload(payload)
        assert formatted_payload == {"password": "[masked]", "file_content": "a" * 100}

    def test__populate_detail_with_host_header(self):
        payload = {"key": "value"}
        self.request.method = "POST"
        self.request.scope = {"type": "http", "headers": {"host": "example.com"}}
        self.request.url.path = "/path"
        self.request.state.request_id = "request_id"
        self.logger_handler.service_name = "service"
        detail = self.logger_handler._populate_detail(payload)
        expected_detail = {
            "service_name": "service",
            "method": "POST",
            "scheme": "http",
            "host": "example.com",
            "endpoint": "/path",
            "payload": {"key": "value"},
            "x-forwarded-for": None,
            "request_id": "request_id",
        }
        assert detail == expected_detail
