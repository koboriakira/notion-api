from lotion.properties import Title


class RecipeTitle(Title):
    NAME = "名前"

    def __init__(self, text: str) -> None:
        super().__init__(
            name=self.NAME,
            text=text,
        )
