from pydantic import BaseModel


class AddRecipeRequest(BaseModel):
    description: str
    reference_url: str | None = None
    slack_channel: str | None = None
