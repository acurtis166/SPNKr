"""Tests for custom error classes."""

from spnkr.errors import (
    APIAuthenticationError,
    APIAuthorizationError,
    APIError,
    APINotFoundError,
    APIRateLimitError,
    APIServerError,
    InvalidXuidError,
    OAuth2Error,
    SPNKrError,
)


class TestSPNKrErrorHierarchy:
    """Test error class hierarchy."""

    def test_oauth2_error_is_spnkr_error(self):
        """OAuth2Error should be a subclass of SPNKrError."""
        assert issubclass(OAuth2Error, SPNKrError)

    def test_invalid_xuid_error_is_spnkr_error(self):
        """InvalidXuidError should be a subclass of SPNKrError."""
        assert issubclass(InvalidXuidError, SPNKrError)

    def test_invalid_xuid_error_is_value_error(self):
        """InvalidXuidError should be a subclass of ValueError."""
        assert issubclass(InvalidXuidError, ValueError)

    def test_api_error_is_spnkr_error(self):
        """APIError should be a subclass of SPNKrError."""
        assert issubclass(APIError, SPNKrError)

    def test_api_specific_errors_are_api_errors(self):
        """All API-specific errors should be subclasses of APIError."""
        assert issubclass(APIAuthenticationError, APIError)
        assert issubclass(APIAuthorizationError, APIError)
        assert issubclass(APINotFoundError, APIError)
        assert issubclass(APIRateLimitError, APIError)
        assert issubclass(APIServerError, APIError)


class TestOAuth2Error:
    """Test OAuth2Error class."""

    def test_oauth2_error_with_error_and_description(self):
        """OAuth2Error should format error and description."""
        error = OAuth2Error(
            {"error": "invalid_grant", "error_description": "Invalid credentials"}
        )
        assert "invalid_grant" in str(error)
        assert "Invalid credentials" in str(error)

    def test_oauth2_error_with_only_error(self):
        """OAuth2Error should work with just error field."""
        error = OAuth2Error({"error": "invalid_scope"})
        assert "invalid_scope" in str(error)
        assert error.response_data == {"error": "invalid_scope"}

    def test_oauth2_error_stores_response_data(self):
        """OAuth2Error should store the response data."""
        data = {"error": "server_error"}
        error = OAuth2Error(data)
        assert error.response_data == data


class TestInvalidXuidError:
    """Test InvalidXuidError class."""

    def test_invalid_xuid_error_with_string(self):
        """InvalidXuidError should handle string XUIDs."""
        error = InvalidXuidError("invalid-xuid")
        assert "invalid-xuid" in str(error)
        assert error.xuid == "invalid-xuid"

    def test_invalid_xuid_error_with_int(self):
        """InvalidXuidError should handle integer XUIDs."""
        error = InvalidXuidError(12345)
        assert "12345" in str(error)
        assert error.xuid == 12345


class TestAPIError:
    """Test APIError class."""

    def test_api_error_message_only(self):
        """APIError should work with message only."""
        error = APIError("Request failed")
        assert "Request failed" in str(error)
        assert error.status_code is None
        assert error.response_data is None

    def test_api_error_with_status_code(self):
        """APIError should include status code in message."""
        error = APIError("Bad request", status_code=400)
        assert "[400]" in str(error)
        assert "Bad request" in str(error)
        assert error.status_code == 400

    def test_api_error_with_response_data(self):
        """APIError should store response data."""
        data = {"error": "validation error"}
        error = APIError("Invalid input", status_code=400, response_data=data)
        assert error.response_data == data


class TestAPISpecificErrors:
    """Test API-specific error classes."""

    def test_api_authentication_error(self):
        """APIAuthenticationError should be raised for 401."""
        error = APIAuthenticationError("Unauthorized", status_code=401)
        assert "[401]" in str(error)
        assert isinstance(error, APIError)

    def test_api_authorization_error(self):
        """APIAuthorizationError should be raised for 403."""
        error = APIAuthorizationError("Forbidden", status_code=403)
        assert "[403]" in str(error)
        assert isinstance(error, APIError)

    def test_api_not_found_error(self):
        """APINotFoundError should be raised for 404."""
        error = APINotFoundError("Not found", status_code=404)
        assert "[404]" in str(error)
        assert isinstance(error, APIError)

    def test_api_rate_limit_error(self):
        """APIRateLimitError should be raised for 429."""
        error = APIRateLimitError("Too many requests", status_code=429)
        assert "[429]" in str(error)
        assert isinstance(error, APIError)

    def test_api_server_error(self):
        """APIServerError should be raised for 5xx."""
        error = APIServerError("Internal server error", status_code=500)
        assert "[500]" in str(error)
        assert isinstance(error, APIError)
