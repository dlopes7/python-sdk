from numbers import Number
from typing import Optional

from open_feature.errors import Reason
from open_feature.flag_evaluation import EvaluationContext, FlagEvaluationDetails
from open_feature.metadata import Metadata
from open_feature.provider import AbstractProvider


class CustomProvider(AbstractProvider):

    def __init__(self):
        self.storage = {}

    @property
    def metadata(self) -> Metadata:
        return Metadata("CustomProvider")

    def resolve_boolean_flag(self,
                             key: str,
                             default: bool,
                             context: Optional[EvaluationContext] = None) -> FlagEvaluationDetails:
        return FlagEvaluationDetails(
            key=key,
            value=bool(self.storage.get(key, default)),
            reason=Reason.DEFAULT,
        )

    def resolve_string_flag(self,
                            key: str,
                            default: str,
                            context: Optional[EvaluationContext] = None) -> FlagEvaluationDetails:
        return FlagEvaluationDetails(
            key=key,
            value=str(self.storage.get(key, default)),
            reason=Reason.DEFAULT,
        )

    def resolve_number_flag(self,
                            key: str,
                            default: Number,
                            context: Optional[EvaluationContext] = None) -> FlagEvaluationDetails:
        return FlagEvaluationDetails(
            key=key,
            value=float(self.storage.get(key, default)),
            reason=Reason.DEFAULT,
        )

    def resolve_dict_flag(self,
                          key: str,
                          default: dict,
                          context: Optional[EvaluationContext] = None) -> FlagEvaluationDetails:
        return FlagEvaluationDetails(
            key=key,
            value=dict(self.storage.get(key, default)),
            reason=Reason.DEFAULT,
        )