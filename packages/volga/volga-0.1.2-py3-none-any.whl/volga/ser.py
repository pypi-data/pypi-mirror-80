from typing import Protocol


class Serializer(Protocol):
    def __serialize__(self) -> None:
        ...
