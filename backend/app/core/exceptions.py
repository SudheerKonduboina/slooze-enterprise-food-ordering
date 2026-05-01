"""Application exception classes and exception handlers."""

from fastapi import HTTPException, status


class SloozeException(Exception):
    """Base exception for Slooze application."""

    def __init__(self, message: str, status_code: int = 500):
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)


class AuthenticationError(SloozeException):
    """Raised when authentication fails."""

    def __init__(self, message: str = "Invalid credentials"):
        super().__init__(message=message, status_code=status.HTTP_401_UNAUTHORIZED)


class AuthorizationError(SloozeException):
    """Raised when user lacks permission."""

    def __init__(self, message: str = "Insufficient permissions"):
        super().__init__(message=message, status_code=status.HTTP_403_FORBIDDEN)


class CountryAccessError(SloozeException):
    """Raised when user tries to access resources from another country."""

    def __init__(self, message: str = "You cannot access resources outside your assigned country"):
        super().__init__(message=message, status_code=status.HTTP_403_FORBIDDEN)


class ResourceNotFoundError(SloozeException):
    """Raised when a requested resource is not found."""

    def __init__(self, resource: str = "Resource", identifier: str = ""):
        message = f"{resource} not found"
        if identifier:
            message = f"{resource} with id '{identifier}' not found"
        super().__init__(message=message, status_code=status.HTTP_404_NOT_FOUND)


class OrderError(SloozeException):
    """Raised for order-related errors."""

    def __init__(self, message: str = "Order operation failed"):
        super().__init__(message=message, status_code=status.HTTP_400_BAD_REQUEST)


class PaymentError(SloozeException):
    """Raised for payment-related errors."""

    def __init__(self, message: str = "Payment operation failed"):
        super().__init__(message=message, status_code=status.HTTP_400_BAD_REQUEST)
