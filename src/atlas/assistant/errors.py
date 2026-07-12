"""Stable assistant errors suitable for user-facing clients."""


class ModelProviderError(Exception):
    def __init__(self, code: str, message: str) -> None:
        super().__init__(message)
        self.code = code
        self.message = message
