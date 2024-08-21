from pydantic import BaseModel


class PostAccountBookRequest(BaseModel):
    title: str
    price: int
    is_fixed_cost: bool | None = None  # 固定費
    category: str | None = None  # 費目
    tag: list[str] | None = None  # タグ
