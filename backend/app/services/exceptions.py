# SessionsAPI
class SessionError(Exception):
    """Base exception for session service errors"""

    pass


class SessionNotFoundError(SessionError):
    """Raised when session is not found"""

    pass


# ChainsAPI
class ChainError(Exception):
    """Base exception for chain service errors"""

    pass


class ChainNotFoundError(ChainError):
    """Raised when chain is not found"""

    pass


# ConfigurationsAPI
class ConfigurationError(Exception):
    """Base exception for configuration service errors"""

    pass


class SessionNotFoundError(ConfigurationError):
    """Raised when session is not found"""

    pass


class ConfigurationNotFoundError(ConfigurationError):
    """Raised when configuration is not found"""

    pass
