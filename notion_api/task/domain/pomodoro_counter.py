from lotion.properties import Number


class PomodoroCounter(Number):
    NAME = "ポモドーロカウンター"
    def __init__(self, number: int = 0) -> None:
        super().__init__(
            name=self.NAME,
            number=number,
        )
