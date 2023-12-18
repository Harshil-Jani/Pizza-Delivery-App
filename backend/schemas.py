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


class Settings(BaseModel):
    authjwt_secret_key: str = (
        "b4bb9013c1c03b29b9311ec0df07f3b0d8fd13edd02d5c45b2fa7b86341fa405"
    )


class LoginModel(BaseModel):
    username: str
    password: str
