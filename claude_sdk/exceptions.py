"""
Exception classes for the Claude SDK.
"""

class ClaudeAPIError(Exception):
    """
    Base exception for all API-related errors.
    """
    
    def __init__(self, message, status_code=None, error_type=None, error_detail=None):
        self.status_code = status_code
        self.error_type = error_type
        self.error_detail = error_detail
        self.message = message
        super().__init__(self.message)
    
    def __str__(self):
        if self.status_code:
            return f"[{self.status_code}] {self.message}"
        return self.message


class RateLimitError(ClaudeAPIError):
    """
    Rate limit exceeded error.
    """
    
    def __init__(self, message="Rate limit exceeded", status_code=429, **kwargs):
        super().__init__(message, status_code, "rate_limit_exceeded", **kwargs)


class InvalidRequestError(ClaudeAPIError):
    """
    Invalid request error.
    """
    
    def __init__(self, message="Invalid request", status_code=400, **kwargs):
        super().__init__(message, status_code, "invalid_request", **kwargs)


class AuthenticationError(ClaudeAPIError):
    """
    Authentication error.
    """
    
    def __init__(self, message="Authentication failed", status_code=401, **kwargs):
        super().__init__(message, status_code, "authentication_error", **kwargs)


class PermissionError(ClaudeAPIError):
    """
    Permission error.
    """
    
    def __init__(self, message="Permission denied", status_code=403, **kwargs):
        super().__init__(message, status_code, "permission_error", **kwargs)


class ResourceNotFoundError(ClaudeAPIError):
    """
    Resource not found error.
    """
    
    def __init__(self, message="Resource not found", status_code=404, **kwargs):
        super().__init__(message, status_code, "resource_not_found", **kwargs)


class ServiceUnavailableError(ClaudeAPIError):
    """
    Service unavailable error.
    """
    
    def __init__(self, message="Service unavailable", status_code=503, **kwargs):
        super().__init__(message, status_code, "service_unavailable", **kwargs)


class ModelNotAvailableError(ClaudeAPIError):
    """
    Model not available error.
    """
    
    def __init__(self, message="Model not available", status_code=404, **kwargs):
        super().__init__(message, status_code, "model_not_available", **kwargs)


class ContentPolicyViolationError(ClaudeAPIError):
    """
    Content policy violation error.
    """
    
    def __init__(self, message="Content violates policies", status_code=400, **kwargs):
        super().__init__(message, status_code, "content_policy", **kwargs)


def handle_api_error(status_code, error_data):
    """
    Handle API error response and raise appropriate exception.
    
    Args:
        status_code (int): HTTP status code
        error_data (dict): Error data from API response
        
    Raises:
        Appropriate exception class based on the error
    """
    error_type = error_data.get("type", "")
    error_message = error_data.get("message", "Unknown error")
    
    if status_code == 400:
        if "violate" in error_message.lower() and "policy" in error_message.lower():
            raise ContentPolicyViolationError(error_message, status_code, error_detail=error_data)
        raise InvalidRequestError(error_message, status_code, error_detail=error_data)
    elif status_code == 401:
        raise AuthenticationError(error_message, status_code, error_detail=error_data)
    elif status_code == 403:
        raise PermissionError(error_message, status_code, error_detail=error_data)
    elif status_code == 404:
        if "model" in error_message.lower():
            raise ModelNotAvailableError(error_message, status_code, error_detail=error_data)
        raise ResourceNotFoundError(error_message, status_code, error_detail=error_data)
    elif status_code == 429:
        raise RateLimitError(error_message, status_code, error_detail=error_data)
    elif status_code >= 500:
        raise ServiceUnavailableError(error_message, status_code, error_detail=error_data)
    else:
        raise ClaudeAPIError(error_message, status_code, error_type, error_detail=error_data)