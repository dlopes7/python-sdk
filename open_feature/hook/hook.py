import logging
from abc import abstractmethod
from dataclasses import dataclass
from numbers import Number
from typing import Union, Optional

from open_feature.flag_evaluation import EvaluationContext, FlagEvaluationDetails, FlagType
from open_feature.logger import default_log
from open_feature.metadata import Metadata


@dataclass
class HookContext:
    flag_key: str
    flag_type: FlagType
    default: Union[bool, str, Number, dict]
    context: EvaluationContext
    client_metadata: Optional[Metadata] = None
    provider_metadata: Optional[Metadata] = None
    log: logging.Logger = default_log


class Hook:
    @abstractmethod
    def before(self, hook_context: HookContext, hints: dict) -> EvaluationContext:
        """
        Runs before flag is resolved.

        :param hook_context: Information about the particular flag evaluation
        :param hints: An immutable mapping of data for users to
        communicate to the hook.
        :return: An EvaluationContext. It will be merged with the
        EvaluationContext instances from other hook, the client and API.
        """
        pass

    @abstractmethod
    def after(
        self, hook_context: HookContext, details: FlagEvaluationDetails, hints: dict
    ):
        """
        Runs after a flag is resolved.

        :param hook_context: Information about the particular flag evaluation
        :param details: Information about how the flag was resolved,
        including any resolved values.
        :param hints: A mapping of data for users to communicate to the hook.
        """
        pass

    @abstractmethod
    def error(self, hook_context: HookContext, exception: Exception, hints: dict):
        """
        Run when evaluation encounters an error. Errors thrown will be swallowed.

        :param hook_context: Information about the particular flag evaluation
        :param exception: The exception that was thrown
        :param hints: A mapping of data for users to communicate to the hook.
        """
        pass

    @abstractmethod
    def finally_after(self, hook_context: HookContext, hints: dict):
        """
        Run after flag evaluation, including any error processing.
        This will always run. Errors will be swallowed.

        :param hook_context: Information about the particular flag evaluation
        :param hints: A mapping of data for users to communicate to the hook.
        """
        pass

    @abstractmethod
    def supports_flag_value_type(self, flag_type: FlagType) -> bool:
        """
        Check to see if the hook supports the particular flag type.

        :param flag_type: particular type of the flag
        :return: a boolean containing whether the flag type is supported (True)
        or not (False)
        """
        return True
