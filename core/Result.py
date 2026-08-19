# core/result.py (أو core/Result.py)

from typing import Generic, TypeVar, Optional, Union

T = TypeVar("T")

class Result(Generic[T]):
    def __init__(self, is_success: bool, value: Optional[T] = None, error: Optional[Union[Exception, str]] = None):
        self.is_success = is_success
        self.value = value
        self.error = error

    @classmethod
    def success(cls, value: T) -> "Result[T]":
        return cls(is_success=True, value=value, error=None)

    @classmethod
    def failure(cls, error: Union[Exception, str]) -> "Result[Exception]":
        return cls(is_success=False, value=None, error=error)