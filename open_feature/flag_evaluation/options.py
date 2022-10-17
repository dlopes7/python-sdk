from __future__ import annotations

from datetime import datetime
from numbers import Number
from typing import List, Dict, Union, TYPE_CHECKING

if TYPE_CHECKING:
    # Avoid circular dependency
    from open_feature.hook import Hook


class FlagEvaluationOptions:
    def __init__(self, hooks: List[Hook], hook_hints: Dict[str, Union[str, Number, bool, datetime, Dict]]):
        self.hooks = hooks
        self._hook_hints = hook_hints

    @property
    def hook_hints(self) -> Dict[str, Union[str, Number, bool, datetime, Dict]]:
        return self._hook_hints
