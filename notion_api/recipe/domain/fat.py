from lotion.properties import Number


class Fat(Number):
    NAME = "F:脂質"

    def __init__(self, number: int = 0) -> None:
        super().__init__(
            name=self.NAME,
            number=number,
        )
