class AppError(Exception):
    """Base domain error for the application."""


class ConflictError(AppError):
    """Raised when a resource already exists."""


class UnauthorizedError(AppError):
    """Raised when credentials are invalid or missing."""


class ForbiddenError(AppError):
    """Raised when current user does not have enough permissions."""


class NotFoundError(AppError):
    """Raised when requested entity is not found."""


class ExternalServiceError(AppError):
    """Raised when external service returns an error."""
