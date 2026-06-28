from api.api_manager import ApiManager
from models.user_data import LoginUserResponse, RegisterUserResponse


class TestAuthApi:
    def test_register_user(self, api_manager: ApiManager, test_user):
        response = api_manager.auth_api.register_user(test_user)
        assert response.status_code == 201, "Ошибка регистрации пользователя"

        register_user_response = RegisterUserResponse.model_validate(response.json())
        assert register_user_response.email == test_user.email, "Email не совпадает"
        assert register_user_response.id != "", "Id пользователя отсутствует в ответе"
        assert register_user_response.roles == test_user.roles, "Роль USER должна быть у пользователя"

    def test_login_user(self, api_manager: ApiManager, registered_user):
        response = api_manager.auth_api.login_user(
            registered_user.email,
            registered_user.password
        )
        assert response.status_code == 201, "Пользователь не найден"

        login_user_response = LoginUserResponse.model_validate(response.json())
        assert login_user_response.accessToken != "", "Токен не должен быть пустым"
