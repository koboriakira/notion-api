from lotion.properties import Checkbox


class DoTommorowFlag(Checkbox):
    NAME = "_明日やるチェック"

    def __init__(self, _checked: bool | None = None) -> None:
        super().__init__(
            name=self.NAME,
            checked=_checked or False,
        )

    @classmethod
    def true(cls) -> "DoTommorowFlag":
        return DoTommorowFlag(_checked=True)

    @classmethod
    def false(cls) -> "DoTommorowFlag":
        return DoTommorowFlag(_checked=False)
