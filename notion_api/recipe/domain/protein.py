from lotion.properties import Number


class Protein(Number):
    NAME = "P:タンパク質"

    def __init__(self, number: int = 0) -> None:
        super().__init__(
            name=self.NAME,
            number=number,
        )
