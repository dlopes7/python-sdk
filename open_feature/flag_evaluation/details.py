from numbers import Number
from typing import Union, Optional

from open_feature.errors import ErrorCode, Reason


class FlagEvaluationDetails:
    def __init__(
        self,
        key: str,
        value: Union[bool, str, Number, dict],
        reason: Reason,
        error_code: Optional[ErrorCode] = None,
        error_message: Optional[str] = None,
        variant:  Optional[Union[bool, str, Number, dict]] = None,
    ):
        self.key = key
        self.value = value
        self.reason = reason
        self.error_code = error_code
        self.variant = variant
