from lotion.properties import Checkbox


class ToBuyFlag(Checkbox):
    NAME = "買う"

    def __init__(self, _checked: bool | None = None) -> None:
        super().__init__(
            name=self.NAME,
            checked=_checked or False,
        )

    @classmethod
    def true(cls) -> "ToBuyFlag":
        return ToBuyFlag(_checked=True)

    @classmethod
    def false(cls) -> "ToBuyFlag":
        return ToBuyFlag(_checked=False)
