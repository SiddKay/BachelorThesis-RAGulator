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


# QuestionsAPI
class QuestionError(Exception):
    """Base exception for question service errors"""

    pass


class QuestionNotFoundError(QuestionError):
    """Raised when question is not found"""

    pass


class SessionNotFoundError(QuestionError):
    """Raised when session is not found"""

    pass


# AnswersAPI
class AnswerError(Exception):
    """Base exception for answer service errors"""

    pass


class AnswerNotFoundError(AnswerError):
    """Raised when answer is not found"""

    pass


class ChainNotFoundError(AnswerError):
    """Raised when chain is not found"""

    pass


class ConfigurationNotFoundError(AnswerError):
    """Raised when configuration is not found"""

    pass


class QuestionNotFoundError(AnswerError):
    """Raised when question is not found"""

    pass
