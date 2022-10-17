from __future__ import annotations
from abc import abstractmethod, ABC
from numbers import Number
from typing import List, Optional

from open_feature.flag_evaluation import EvaluationContext, FlagEvaluationDetails
from open_feature.hook.hook import Hook
from open_feature.metadata import Metadata


class AbstractProvider(ABC):
    _instance: AbstractProvider

    @property
    @abstractmethod
    def metadata(self) -> Metadata:
        raise NotImplementedError

    def __new__(cls, *args, **kwargs):
        # Singleton, always return the same instance
        # We need to use getattr because provider implementations don't need to declare _instance
        if getattr(cls, "_instance", None) is None:
            setattr(cls, "_instance", super(AbstractProvider, cls).__new__(cls, *args, **kwargs))
        return cls._instance

    @property
    def hooks(self) -> List[Hook]:
        return []

    @abstractmethod
    def resolve_boolean_flag(
        self,
        key: str,
        default: bool,
        context: Optional[EvaluationContext] = None,
    ) -> FlagEvaluationDetails:
        raise NotImplementedError

    @abstractmethod
    def resolve_string_flag(
        self,
        key: str,
        default: str,
        context: Optional[EvaluationContext] = None,
    ) -> FlagEvaluationDetails:
        raise NotImplementedError

    @abstractmethod
    def resolve_number_flag(
        self,
        key: str,
        default: Number,
        context: Optional[EvaluationContext] = None,
    ) -> FlagEvaluationDetails:
        raise NotImplementedError

    @abstractmethod
    def resolve_dict_flag(
        self,
        key: str,
        default: dict,
        context: Optional[EvaluationContext] = None,
    ) -> FlagEvaluationDetails:
        raise NotImplementedError
