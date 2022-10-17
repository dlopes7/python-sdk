from typing import Optional, List, Any, Dict, Union
from logging import Logger
from numbers import Number


import open_feature as api
from open_feature.hook import Hook, HookContext
from open_feature.flag_evaluation import FlagEvaluationDetails, EvaluationContext, FlagEvaluationOptions, FlagType
from open_feature.errors import OpenFeatureError, GeneralError, ErrorCode, Reason
from open_feature.logger import default_log
from open_feature.metadata import Metadata
from open_feature.provider import AbstractProvider, NoOpProvider


class OpenFeatureClient:
    def __init__(
        self,
        name: str,
        version: str,
        context: Optional[EvaluationContext] = None,
        hooks: Optional[List[Hook]] = None,
        provider: Optional[AbstractProvider] = None,
        log: Optional[Logger] = None,
    ):

        if context is None:
            context = EvaluationContext()
        self._context = context

        if hooks is None:
            hooks = []
        self._hooks = hooks

        if provider is None:
            provider = NoOpProvider()
        self._provider = provider

        if log is None:
            log = default_log
        self._log = log

        self._metadata = Metadata(name, version)

    @property
    def metadata(self) -> Metadata:
        return self._metadata

    def add_hooks(self, hooks: List[Hook]):
        self._hooks.extend(hooks)

    def clear_hooks(self):
        self._hooks = []

    def get_boolean_value(
        self,
        key: str,
        default: bool,
        context: Optional[EvaluationContext] = None,
        options: Optional[FlagEvaluationOptions] = None
    ) -> bool:
        return self.get_boolean_details(key, default, context, options).value

    def get_boolean_details(
        self,
        key: str,
        default: bool,
        context: Optional[EvaluationContext] = None,
        options: Optional[FlagEvaluationOptions] = None,
    ) -> FlagEvaluationDetails:
        return self._evaluate(FlagType.BOOLEAN, key, default, context, options)

    def get_string_value(
        self,
        key: str,
        default: str,
        context: Optional[EvaluationContext] = None,
        options: Optional[FlagEvaluationOptions] = None,
    ) -> str:
        return self.get_string_details(key, default, context, options).value

    def get_string_details(
        self,
        key: str,
        default: str,
        context: Optional[EvaluationContext] = None,
        options: Optional[FlagEvaluationOptions] = None,
    ) -> FlagEvaluationDetails:
        return self._evaluate(FlagType.STRING, key, default, context, options)

    def get_number_value(
        self,
        key: str,
        default: Number,
        context: Optional[EvaluationContext] = None,
        options: Optional[FlagEvaluationOptions] = None,
    ) -> Number:
        return self.get_number_details(
            key,
            default,
            context,
            options,
        ).value

    def get_number_details(
        self,
        key: str,
        default: Number,
        context: Optional[EvaluationContext] = None,
        options: Optional[FlagEvaluationOptions] = None,
    ) -> FlagEvaluationDetails:
        return self._evaluate(FlagType.NUMBER, key, default, context, options)

    def get_dict_value(
        self,
        key: str,
        default: Dict,
        context: EvaluationContext = None,
        options: Optional[FlagEvaluationOptions] = None,
    ) -> Dict:
        return self.get_dict_details(key, default, context, options).value

    def get_dict_details(
        self,
        key: str,
        default: Dict,
        context: EvaluationContext = None,
        options: Optional[FlagEvaluationOptions] = None,
    ) -> FlagEvaluationDetails:
        return self._evaluate(FlagType.DICT, key, default, context, options)

    def _evaluate(
        self,
        flag_type: FlagType,
        key: str,
        default: Any,
        invocation_context: EvaluationContext = None,
        options: Optional[FlagEvaluationOptions] = None,
    ) -> FlagEvaluationDetails:
        """
        Evaluate the flag requested by the user from the client's provider.

        :param flag_type: the type of the flag being returned
        :param key: the string key of the selected flag
        :param default: backup value returned if no result found by the provider
        :param invocation_context: Information for the purposes of flag evaluation
        :param options: Additional flag evaluation information
        :return: a FlagEvaluationDetails object with the fully evaluated flag from a
        provider
        """

        if invocation_context is None:
            invocation_context = EvaluationContext()

        if options is None:
            options = FlagEvaluationOptions([], {})

        # These are all possible hooks that we need to run

        hooks = [
            *api.open_feature.hooks,
            *self._hooks,
            *options.hooks,
            *self._provider.hooks
        ]

        # Also store the hooks in reversed order, they are needed for hooks other than "before"
        reversed_hooks = list(reversed(hooks))

        # Merge all contexts into one, note that the order matters.
        # If there are duplicate keys the last context defined here will win
        merged_context = EvaluationContext({
            **api.open_feature.context,
            # **api.open_feature.transaction_context,
            **self._context,
            **invocation_context
        })

        # The hook context is later used for hooks during their execution
        hook_context = HookContext(
            flag_key=key,
            default=default,
            flag_type=flag_type,
            context=merged_context,
            client_metadata=self._metadata,
            provider_metadata=self._provider.metadata,
            log=self._log,
        )

        try:
            # Run the before method of all hooks, note that this can raise any Exception
            eval_context = self._before_hooks(hooks, hook_context, options)

            # Evaluate the flag after running the before hooks
            flag_evaluation = self._provider_evaluate(flag_type, key, default, eval_context)

            # Run the after method of all hooks, this is never reached if an Exception was raised
            # Note that hooks here run in reversed order
            self._after_hooks(reversed_hooks, hook_context, flag_evaluation, options)

            return flag_evaluation


        except Exception as e:  # noqa
            # If an exception is raised in any hooks (user defined), catch them, run the error hooks
            # and return a flag evaluation with the exception details
            self._error_hooks(reversed_hooks, hook_context, e, options)

            error_code = ErrorCode.GENERAL
            if isinstance(e, OpenFeatureError):
                error_code = e.error_code

            return FlagEvaluationDetails(
                key=key,
                value=default,
                reason=Reason.ERROR,
                error_code=error_code,
                error_message=repr(e),
            )

        finally:
            # Run the finally_after method of all hooks, this is always reached
            self._finally_hooks(reversed_hooks, hook_context, options)

    def _provider_evaluate(
        self,
        flag_type: FlagType,
        key: str,
        default: Union[bool, str, Number, Dict],
        context: EvaluationContext = None,
    ) -> FlagEvaluationDetails:
        """
        Encapsulated method to create a FlagEvaluationDetail from a specific provider.

        :param flag_type: the type of the flag being returned
        :param key: the string key of the selected flag
        :param default: backup value returned if no result found by the provider
        :param context: Information for the purposes of flag evaluation
        :return: a FlagEvaluationDetails object with the fully evaluated flag from a
        provider
        """

        if flag_type == FlagType.BOOLEAN:
            return self._provider.resolve_boolean_flag(key, default, context)
        elif flag_type == FlagType.NUMBER:
            return self._provider.resolve_number_flag(key, default, context)
        elif flag_type == FlagType.STRING:
            return self._provider.resolve_string_flag(key, default, context)
        elif flag_type == FlagType.DICT:
            return self._provider.resolve_dict_flag(key, default, context)
        else:
            raise GeneralError(f"Unknown flag type: {flag_type}")

    def _before_hooks(self,
                      hooks: List[Hook],
                      hook_context: HookContext,
                      options: FlagEvaluationOptions) -> EvaluationContext:
        for hook in hooks:
            hook.before(hook_context, options.hook_hints)

        self._log.debug(f"finished running before hooks for {hook_context}")
        return hook_context.context

    def _after_hooks(self,
                     hooks: List[Hook],
                     hook_context: HookContext,
                     evaluation_details: FlagEvaluationDetails,
                     options: FlagEvaluationOptions):

        for hook in hooks:
            hook.after(hook_context, evaluation_details, options.hook_hints)

        self._log.debug(f"finished running after hooks for {hook_context}")

    def _error_hooks(self,
                     hooks: List[Hook],
                     hook_context: HookContext,
                     exception: Exception,
                     options: FlagEvaluationOptions):

        for hook in hooks:
            try:
                hook.error(hook_context, exception, options.hook_hints)
            except Exception as e:  # noqa
                self._log.exception(f"Error running after hook: {repr(e)}")

        self._log.debug(f"finished running error hooks for {hook_context}")

    def _finally_hooks(self, hooks: List[Hook], hook_context: HookContext, options: FlagEvaluationOptions):
        for hook in hooks:
            try:
                hook.finally_after(hook_context, options.hook_hints)
            except Exception as e:
                self._log.exception(f"Error running finally hook: {repr(e)}")
        self._log.debug(f"finished running finally hooks for {hook_context}")
