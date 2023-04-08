class ApiRateLimitExceedance(Exception):
    """Raised when an API rate limit is exceeded."""

    def __init__(self, request_limit: int, minutes: int) -> None:
        super().__init__(
            f"API rate limit exceeded. "
            f"Request limit: {request_limit} requests per {minutes} minutes."
        )
