from typing import Any, Literal

from pydantic import BaseModel

class Response(BaseModel):
    status: Literal["success", "error"] = "success"
    data: Any | None = None
    message: str | None = None
