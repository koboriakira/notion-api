from dataclasses import dataclass


@dataclass
class Button:
    type: str = "rollup"


    @staticmethod
    def of() -> "Button":
        return Button()

    def value_for_filter(self) -> str:
        raise NotImplementedError
