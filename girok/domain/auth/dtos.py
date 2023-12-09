from pydantic import BaseModel, Field


class RefreshTokenRequest(BaseModel):
    refresh_token: str = Field(default=...)


class RefreshTokenResponse(BaseModel):
    access_token: str = Field(default=...)
