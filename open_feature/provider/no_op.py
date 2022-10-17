from numbers import Number
from typing import Optional

from open_feature.flag_evaluation import EvaluationContext, FlagEvaluationDetails
from open_feature.errors import  Reason
from open_feature.metadata import Metadata
from open_feature.provider import AbstractProvider

PASSED_IN_DEFAULT = "Passed in default"


class NoOpProvider(AbstractProvider):

    def __init__(self):
        self._metadata = Metadata("NoOpProvider")

    def metadata(self) -> Metadata:
        return self._metadata

    def resolve_boolean_flag(
        self,
        key: str,
        default: bool,
        context: Optional[EvaluationContext] = None,
    ) -> FlagEvaluationDetails:
        return FlagEvaluationDetails(
            key=key,
            value=default,
            reason=Reason.DEFAULT,
            variant=PASSED_IN_DEFAULT,
        )

    def resolve_string_flag(
        self,
        key: str,
        default: str,
        context: Optional[EvaluationContext] = None,
    ) -> FlagEvaluationDetails:
        return FlagEvaluationDetails(
            key=key,
            value=default,
            reason=Reason.DEFAULT,
            variant=PASSED_IN_DEFAULT,
        )

    def resolve_number_flag(
        self,
        key: str,
        default: Number,
        context: Optional[EvaluationContext] = None,
    ) -> FlagEvaluationDetails:
        return FlagEvaluationDetails(
            key=key,
            value=default,
            reason=Reason.DEFAULT,
            variant=PASSED_IN_DEFAULT,
        )

    def resolve_dict_flag(
        self,
        key: str,
        default: dict,
        context: Optional[EvaluationContext] = None,
    ) -> FlagEvaluationDetails:
        return FlagEvaluationDetails(
            key=key,
            value=default,
            reason=Reason.DEFAULT,
            variant=PASSED_IN_DEFAULT,
        )
