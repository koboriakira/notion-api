from lotion.properties import Checkbox


class ImportantFlag(Checkbox):
    NAME = "重要"

    def __init__(self, _checked: bool | None = None) -> None:
        super().__init__(
            name=self.NAME,
            checked=_checked or False,
        )

    @classmethod
    def true(cls) -> "ImportantFlag":
        return ImportantFlag(_checked=True)

    @classmethod
    def false(cls) -> "ImportantFlag":
        return ImportantFlag(_checked=False)
