from pydantic import BaseModel, EmailStr, Field


class UserLogin(BaseModel):
    email: EmailStr = Field(..., min_length=1, max_length=50)
    password: str = Field(..., min_length=8, max_length=50)


class CreateUserBase(BaseModel):
    first_name: str = Field(..., min_length=1, max_length=50)
    last_name: str = Field(..., min_length=1, max_length=50)
    email: EmailStr = Field(..., min_length=1, max_length=50)
    password: str = Field(..., min_length=8, max_length=50)
    role: str = Field(default="client")


class RetrieveUserBase(BaseModel):
    user_id: int
    first_name: str
    last_name: str
    email: EmailStr
    role: str
    model_config = {"from_attributes": True}
