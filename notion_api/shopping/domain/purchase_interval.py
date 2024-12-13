from lotion.properties import Number


class PurchaseInterval(Number):
    NAME = "購入間隔"

    def __init__(self, number: int = 0) -> None:
        super().__init__(
            name=self.NAME,
            number=number,
        )
