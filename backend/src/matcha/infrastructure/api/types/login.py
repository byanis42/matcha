from pydantic import BaseModel

class AccessToken(BaseModel):
    access_token: str
    refresh_token: str
