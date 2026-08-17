from pydantic import BaseModel, Field

class RefreshTokenSchema(BaseModel):
    refresh_token: str = Field(..., description="Valid JWT Refresh Token")
