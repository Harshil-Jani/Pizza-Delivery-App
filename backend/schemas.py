from pydantic import BaseModel
from typing import Optional


class SignUpUser(BaseModel):
    id: Optional[int]
    username: str
    password: str
    email: str
    is_staff: Optional[bool] = False
    is_active: Optional[bool] = True

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "username": "test",
                "password": "test",
                "email": "test@gmail.com",
                "is_staff": False,
                "is_active": True,
            }
        }
