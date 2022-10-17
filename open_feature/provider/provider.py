from abc import abstractmethod, ABC
from numbers import Number
from typing import List, Optional

from open_feature.flag_evaluation import EvaluationContext
from open_feature.hook.hook import Hook
from open_feature.metadata import Metadata


class AbstractProvider(ABC):
    @property
    @abstractmethod
    def metadata(self) -> Metadata:
        raise NotImplementedError

    @property
    def hooks(self) -> List[Hook]:
        return []

    @abstractmethod
    def resolve_boolean_flag(
        self,
        key: str,
        default: bool,
        context: Optional[EvaluationContext] = None,
    ):
        raise NotImplementedError

    @abstractmethod
    def resolve_string_flag(
        self,
        key: str,
        default: str,
        context: Optional[EvaluationContext] = None,
    ):
        raise NotImplementedError

    @abstractmethod
    def resolve_number_flag(
        self,
        key: str,
        default: Number,
        context: Optional[EvaluationContext] = None,
    ):
        raise NotImplementedError

    @abstractmethod
    def resolve_dict_flag(
        self,
        key: str,
        default: dict,
        context: Optional[EvaluationContext] = None,
    ):
        raise NotImplementedError
