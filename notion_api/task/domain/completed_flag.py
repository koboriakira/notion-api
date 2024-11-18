from notion_client_wrapper.properties.checkbox import Checkbox


class CompletedFlag(Checkbox):
    NAME = "_完了チェック"

    def __init__(self, _checked: bool | None = None) -> None:
        super().__init__(
            name=self.NAME,
            checked=_checked or False,
        )

    @classmethod
    def true(cls) -> "CompletedFlag":
        return CompletedFlag(_checked=True)

    @classmethod
    def false(cls) -> "CompletedFlag":
        return CompletedFlag(_checked=False)
