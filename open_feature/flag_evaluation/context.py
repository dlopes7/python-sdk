from collections import UserDict


class EvaluationContext(UserDict):
    def __init__(self, /, values: dict = None, targeting_key: str = None, **kwargs):
        super().__init__(values, **kwargs)
        self.targeting_key = targeting_key
