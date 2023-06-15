from src.common.exception.http_error import HTTPError, HTTPUnprocessableEntityError, HTTPInternalServerError


class TestHTTPError:
    def test_http_error(self):
        http_error = HTTPError(404, "NOT_FOUND", "Page not found")
        print(http_error.detail)
        assert http_error.http_status == 404
        assert http_error.error_code == "NOT_FOUND"
        assert http_error.message == "Page not found"
        assert http_error.detail is not None

    def test_http_error_with_detail(self):
        detail = {"user_id": 1234, "name": "John"}
        http_error = HTTPError(
            404, "NOT_FOUND", "Page not found", detail
        )
        assert http_error.http_status == 404
        assert http_error.error_code == "NOT_FOUND"
        assert http_error.message == "Page not found"
        assert http_error.detail == detail


class TestHTTPUnprocessableEntityError:
    def test_http_unprocessable_entity_error(self):
        http_unprocessable_entity_error = HTTPUnprocessableEntityError(
            "VALIDATION_ERROR", "Validation failed"
        )
        assert http_unprocessable_entity_error.http_status == 422
        assert http_unprocessable_entity_error.error_code == "VALIDATION_ERROR"
        assert http_unprocessable_entity_error.message == "Validation failed"
        assert http_unprocessable_entity_error.detail is not None

    def test_http_unprocessable_entity_error_with_detail(self):
        detail = {"email": "test@example.com", "password": "1234"}
        http_unprocessable_entity_error = HTTPUnprocessableEntityError(
            "VALIDATION_ERROR", "Validation failed", detail
        )
        assert http_unprocessable_entity_error.http_status == 422
        assert http_unprocessable_entity_error.error_code == "VALIDATION_ERROR"
        assert http_unprocessable_entity_error.message == "Validation failed"
        assert http_unprocessable_entity_error.detail == detail


class TestHTTPInternalServerError:
    def test_http_internal_server_error(self):
        http_internal_server_error = HTTPInternalServerError(
            "INTERNAL_SERVER_ERROR", "Internal server error"
        )
        assert http_internal_server_error.http_status == 500
        assert http_internal_server_error.error_code == "INTERNAL_SERVER_ERROR"
        assert http_internal_server_error.message == "Internal server error"
        assert http_internal_server_error.detail is not None

    def test_http_internal_server_error_with_detail(self):
        detail = {"error": "Database connection failed"}
        http_internal_server_error = HTTPInternalServerError(
            "INTERNAL_SERVER_ERROR", "Internal server error", detail
        )
        assert http_internal_server_error.http_status == 500
        assert http_internal_server_error.error_code == "INTERNAL_SERVER_ERROR"
        assert http_internal_server_error.message == "Internal server error"
        assert http_internal_server_error.detail == detail
