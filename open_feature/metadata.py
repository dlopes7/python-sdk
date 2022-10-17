class Metadata:

    def __init__(self, name: str, version: str = None):
        self._name = name
        self._version = version

    @property
    def name(self) -> str:
        return self._name

    @property
    def version(self) -> str:
        return self._version
