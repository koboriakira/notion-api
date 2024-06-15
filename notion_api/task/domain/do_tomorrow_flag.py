from notion_client_wrapper.properties.checkbox import Checkbox


class DoTommorowFlag(Checkbox):
    NAME = "明日やる"

    def __init__(self, _checked: bool | None = None) -> None:
        super().__init__(
            name=self.NAME,
            checked=_checked or False,
        )

    @classmethod
    def true(cls: "DoTommorowFlag") -> "DoTommorowFlag":
        return DoTommorowFlag(_checked=True)

    @classmethod
    def false(cls: "DoTommorowFlag") -> "DoTommorowFlag":
        return DoTommorowFlag(_checked=False)
