from lotion.block import Paragraph

MAX_LENGTH = 1500


def split_paragraph(text: str | None) -> list[Paragraph]:
    """テキストを最大文字数で分割する"""
    if text is None:
        return []

    if len(text) <= MAX_LENGTH:
        return [Paragraph.from_plain_text(text=text)]

    paragraph_list: list[Paragraph] = []
    # textが最長文字数を超える場合は分割して追加する
    for i in range(0, len(text), MAX_LENGTH):
        paraphrased_text = text[i : i + MAX_LENGTH]
        paragraph_list.append(Paragraph.from_plain_text(text=paraphrased_text))
    return paragraph_list
