from pydantic import BaseModel
from pydantic import EmailStr
from typing import Literal


class TokenData(BaseModel):
    sub: str
    user_id: int
    first_name: str
    last_name: str
    email: EmailStr
    role: Literal["admin", "user"]
