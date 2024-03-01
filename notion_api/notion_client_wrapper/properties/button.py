from dataclasses import dataclass


@dataclass
class Button():
    type: str = "rollup"


    @staticmethod
    def of() -> "Button":
        return Button()
