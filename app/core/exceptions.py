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

class TokenError(Exception):
    """Base class for token-related errors."""

class InvalidToken(TokenError):
    pass

class TokenAlreadyRevoked(TokenError):
    pass

class TokenExpired(TokenError):
    pass