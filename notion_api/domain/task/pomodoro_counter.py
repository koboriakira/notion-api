from notion_client_wrapper.properties.number import Number


class PomodoroCounter(Number):
    NAME = "実施日"
    def __init__(self, number: int = 0) -> None:
        super().__init__(
            name=self.NAME,
            number=number,
        )
