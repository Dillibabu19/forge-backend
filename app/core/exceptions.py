class AuthError(Exception):
    """Base class for auth-related errors."""


class UserNotFoundError(AuthError):
    pass


class InvalidCredentialsError(AuthError):
    pass


class UserInactiveError(AuthError):
    pass


class UserAlreadyExistsError(AuthError):
    pass
