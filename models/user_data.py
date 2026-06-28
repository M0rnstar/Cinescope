import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr, Field, model_validator, field_validator
from constants.roles import Roles


class UserData(BaseModel):
    email: EmailStr = Field(description="Email пользователя")
    fullName: str = Field(min_length=1, description="Имя, не может быть пустым")
    password: str = Field(min_length=6, description="Пароль, минимум 6 символов")
    passwordRepeat: str = Field(description="Повтор пароля для сверки")
    roles: list[Roles] = Field(description="Список ролей (Enum)")
    banned: Optional[bool] = False
    verified: Optional[bool] = True

    @model_validator(mode="after")
    def passwords_match(self):
        if self.password != self.passwordRepeat:
            raise ValueError("password and passwordRepeat do not match")
        return self

class RegisterUserResponse(BaseModel):
    id: str
    email: str = Field(pattern=r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$")
    fullName: str
    verified: Optional[bool] = None
    banned: Optional[bool] = None
    roles: list[Roles]
    createdAt: str

    @field_validator("createdAt")
    def validate_created_at(cls, value: str) -> str:
        try:
            datetime.datetime.fromisoformat(value)
        except ValueError:
            raise ValueError("Некорректный формат даты и времени")
        return value


class LoginUserResponse(BaseModel):
    accessToken: str = Field(min_length=1)
