from dataclasses import dataclass


@dataclass
class TypeSafeObject:
    def __post_init__(self) -> None:
        for field in self.__annotations__:
            value = getattr(self, field)
            if not isinstance(value, self.__annotations__[field]):
                msg = f"[{type(self)} Invalid type for {field}: {type(value)}"
                raise TypeError(msg)


@dataclass(frozen=True)
class TypeSafeFrozenObject:
    def __post_init__(self) -> None:
        for field in self.__annotations__:
            value = getattr(self, field)
            if not isinstance(value, self.__annotations__[field]):
                msg = f"[{type(self)} Invalid type for {field}: {type(value)}"
                raise TypeError(msg)
