from lotion.properties import Checkbox


class LaterFlag(Checkbox):
    NAME = "_あとでチェック"

    def __init__(self, _checked: bool | None = None) -> None:
        super().__init__(
            name=self.NAME,
            checked=_checked or False,
        )

    @classmethod
    def true(cls) -> "LaterFlag":
        return LaterFlag(_checked=True)

    @classmethod
    def false(cls) -> "LaterFlag":
        return LaterFlag(_checked=False)
