from api.api_manager import ApiManager


class TestAuthApi:
    def test_register_user(self, api_manager: ApiManager, test_user):
        response = api_manager.auth_api.register_user(test_user)

        assert response.status_code == 201, "Ошибка регистрации пользователя"
        response_data = response.json()
        assert response_data["email"] == test_user["email"], "Email не совпадает"
        assert "id" in response_data, "Id пользователя отсутствует в ответе"
        assert "roles" in response_data, "Роли пользователя отсутствуют в ответе"
        assert "USER" in response_data["roles"], "Роль USER должна быть у пользователя"

    def test_login_user(self, api_manager: ApiManager, registered_user):
        response = api_manager.auth_api.login_user(
            registered_user["email"],
            registered_user["password"]
        )
        assert response.status_code == 200, "Пользователь не найден"
        token = response.json().get("accessToken")
        assert token is not None, "Токен доступа отсутствует в ответе"
        assert isinstance(token, str), "Токен должен быть строкой"
        assert token != "", "Токен не должен быть пустым"