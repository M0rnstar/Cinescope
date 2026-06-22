from pydantic import BaseModel, EmailStr, Field, model_validator
from constants.roles import Roles


class UserCreate(BaseModel):
    email: EmailStr = Field(description="Email пользователя")
    fullName: str = Field(min_length=1, description="Имя, не может быть пустым")
    password: str = Field(min_length=6, description="Пароль, минимум 6 символов")
    passwordRepeat: str = Field(description="Повтор пароля для сверки")
    roles: list[Roles] = Field(description="Список ролей (Enum), а не строк")

    @model_validator(mode="after")
    def passwords_match(self):
        if self.password != self.passwordRepeat:
            raise ValueError("password and passwordRepeat do not match")
        return self
