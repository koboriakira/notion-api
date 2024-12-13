from lotion.properties import Checkbox


class IsStarted(Checkbox):
    NAME = "_開始チェック"

    def __init__(self, _checked: bool | None = None) -> None:
        super().__init__(
            name=self.NAME,
            checked=_checked or False,
        )

    @classmethod
    def true(cls) -> "IsStarted":
        return IsStarted(_checked=True)

    @classmethod
    def false(cls) -> "IsStarted":
        return IsStarted(_checked=False)
