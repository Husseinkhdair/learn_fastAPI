from dataclasses import dataclass
from typing import Generic, Optional
from annotated_types import T


@dataclass
class Result(Generic[T]):
    data: Optional[T] = None
    error: Optional[Exception] = None

    @property
    def is_success(self) -> bool:
        return self.error is None