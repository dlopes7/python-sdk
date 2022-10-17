from enum import Enum


class ErrorCode(Enum):
    PROVIDER_NOT_READY = "PROVIDER_NOT_READY"
    FLAG_NOT_FOUND = "FLAG_NOT_FOUND"
    PARSE_ERROR = "PARSE_ERROR"
    TYPE_MISMATCH = "TYPE_MISMATCH"
    TARGETING_KEY_MISSING = "TARGETING_KEY_MISSING"
    INVALID_CONTEXT = "INVALID_CONTEXT"
    GENERAL = "GENERAL"


class Reason(Enum):
    DISABLED = "DISABLED"
    SPLIT = "SPLIT"
    TARGETING_MATCH = "TARGETING_MATCH"
    DEFAULT = "DEFAULT"
    UNKNOWN = "UNKNOWN"
    ERROR = "ERROR"


class OpenFeatureError(Exception):
    """
    A generic open feature exception, this exception should not be raised. Instead
    the more specific exceptions extending this one should be used.
    """

    def __init__(self, error_message: str = None, error_code: ErrorCode = None):
        """
        Constructor for the generic OpenFeatureError.
        @param error_message: a string message representing why the error has been
        raised
        @param error_code: the ErrorCode string enum value for the type of error
        @return: the generic OpenFeatureError exception
        """
        self.error_message = error_message
        self.error_code = error_code


class ProviderNotReadyError(OpenFeatureError):
    """
    Raised when the provider is not ready to be used.
    """

    def __init__(self, error_message: str = None, error_code: ErrorCode = None):
        """
        Constructor for the ProviderNotReady exception, used for ErrorCode.PROVIDER_NOT_READY.
        @param error_message: a string message representing why the error has been
        raised
        @param error_code: the ErrorCode string enum value for the type of error
        @return: the ProviderNotReady exception
        """
        super().__init__(error_message, error_code)


class FlagNotFoundError(OpenFeatureError):
    """
    This exception should be raised when the provider cannot find a flag with the
    key provided by the user.
    """

    def __init__(self, error_message: str = None):
        """
        Constructor for the FlagNotFoundError.  The error code for
        this type of exception is ErrorCode.FLAG_NOT_FOUND.
        @param error_message: a string message representing why the error has been
        raised
        @return: the generic FlagNotFoundError exception
        """
        super().__init__(error_message, ErrorCode.FLAG_NOT_FOUND)


class ParseError(OpenFeatureError):
    """
    This exception should be raised when the flag returned by the provider cannot
    be parsed into a FlagEvaluationDetails object.
    """

    def __init__(self, error_message: str = None):
        """
        Constructor for the ParseError. The error code for this type of exception
        is ErrorCode.PARSE_ERROR.
        @param error_message: a string message representing why the error has been
        raised
        @return: the generic ParseError exception
        """
        super().__init__(error_message, ErrorCode.PARSE_ERROR)


class TypeMismatchError(OpenFeatureError):
    """
    This exception should be raised when the flag returned by the provider does
    not match the type requested by the user.
    """

    def __init__(self, error_message: str = None):
        """
        Constructor for the TypeMismatchError. The error code for this type of
        exception is ErrorCode.TYPE_MISMATCH.
        @param error_message: a string message representing why the error has been
        raised
        @return: the generic TypeMismatchError exception
        """
        super().__init__(error_message, ErrorCode.TYPE_MISMATCH)


class TargetingKeyMissingError(OpenFeatureError):
    """
    This exception should be raised when the flag returned by the provider does
    not have a targeting key.
    """

    def __init__(self, error_message: str = None):
        """
        Constructor for the TargetingKeyMissingError. The error code for this type
        of exception is ErrorCode.TARGETING_KEY_MISSING.
        @param error_message: a string message representing why the error has been
        raised
        @return: the generic TargetingKeyMissingError exception
        """
        super().__init__(error_message, ErrorCode.TARGETING_KEY_MISSING)


class InvalidContextError(OpenFeatureError):
    """
    This exception should be raised when the flag returned by the provider does
    not have a targeting key.
    """

    def __init__(self, error_message: str = None):
        """
        Constructor for the InvalidContextError. The error code for this type
        of exception is ErrorCode.INVALID_CONTEXT.
        @param error_message: a string message representing why the error has been
        raised
        @return: the generic InvalidContextError exception
        """
        super().__init__(error_message, ErrorCode.INVALID_CONTEXT)


class GeneralError(OpenFeatureError):
    """
    This exception should be raised when the for an exception within the open
    feature python sdk.
    """

    def __init__(self, error_message: str = None):
        """
        Constructor for the GeneralError.  The error code for this type of exception
        is ErrorCode.GENERAL.
        @param error_message: a string message representing why the error has been
        raised
        @return: the generic GeneralError exception
        """
        super().__init__(error_message, ErrorCode.GENERAL)
