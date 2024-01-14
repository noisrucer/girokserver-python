from pydantic import BaseModel, Field


class CheckEmailRegisteredRequest(BaseModel):
    is_registered: bool = Field(default=..., examples=[True])
