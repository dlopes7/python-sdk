from logging import Logger
from typing import Optional, List

import open_feature.client as client
from open_feature.flag_evaluation import EvaluationContext
from open_feature.hook import Hook
from open_feature.logger import default_log
from open_feature.provider import AbstractProvider, NoOpProvider


class OpenFeatureApi:

    # Used to store the singleton client instance
    _instance = None

    def __init__(self, log: Optional[Logger] = None):
        self._provider = NoOpProvider()
        self._context = EvaluationContext()
        self._hooks = []

        if log is None:
            log = default_log
        self._log = log

    def __new__(cls, *args, **kwargs):
        # Singleton, always return the same instance
        if cls._instance is None:
            cls._instance = super(OpenFeatureApi, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    @property
    def provider(self) -> AbstractProvider:
        return self._provider

    @provider.setter
    def provider(self, provider: AbstractProvider):
        if provider is None:
            self._log.warning("Provider cannot be None, using NoOpProvider")
            provider = NoOpProvider()

        self._provider = provider

    def client(self,
               name: Optional[str] = None,
               version: Optional[str] = None,
               context: Optional[EvaluationContext] = None,
               log: Logger = default_log) -> client.OpenFeatureClient:
        """
        Get an OpenFeatureClient instance

        :param name: The application name
        :param version: The application version
        :param context: The context to use for flag evaluation
        :param log: The logger to use
        """
        if self.provider is None:
            self._log.warning("Initializing client with NoOpProvider")
        return client.OpenFeatureClient(
            name=name,
            version=version,
            context=context,
            provider=self.provider,
            log=log,
        )

    @property
    def hooks(self) -> List[Hook]:
        return self._hooks

    @property
    def context(self) -> EvaluationContext:
        return self._context

    def add_hooks(self, hooks: List[Hook]):
        self._hooks.extend(hooks)

    def clear_hooks(self):
        self._hooks = []


