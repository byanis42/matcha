from dataclasses import dataclass
from typing import Generic, TypeVar, Protocol

Input = TypeVar("Input")
Output = TypeVar("Output")


@dataclass
class Result(Generic[Output]):
    success: bool
    value: Output | None = None
    error: str | None = None

    @classmethod
    def success(cls, value: Output) -> "Result[Output]":
        return cls(success=True, value=value)

    @classmethod
    def failure(cls, error: str) -> "Result[Output]":
        return cls(success=False, error=error)


class UseCase(Generic[Input, Output], Protocol):
    async def execute(self, input_data: Input) -> Result[Output]: ...
