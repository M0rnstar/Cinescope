import allure
import pytest

from api.api_manager import ApiManager
from models.user_data import LoginUserResponse, RegisterUserResponse


@pytest.mark.api
@pytest.mark.regression
@allure.epic("Cinescope API")
@allure.feature("Авторизация")
class TestAuthApi:
    @pytest.mark.smoke
    @allure.story("Регистрация пользователя")
    @allure.title("Регистрация пользователя с валидными данными")
    @allure.description("Проверка успешной регистрации пользователя и данных в ответе API.")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_register_user(self, api_manager: ApiManager, test_user):
        response = api_manager.auth_api.register_user(test_user)
        assert response.status_code == 201, "Ошибка регистрации пользователя"

        register_user_response = RegisterUserResponse.model_validate(response.json())
        assert register_user_response.email == test_user.email, "Email не совпадает"
        assert register_user_response.id != "", "Id пользователя отсутствует в ответе"
        assert register_user_response.roles == test_user.roles, "Роль USER должна быть у пользователя"

    @pytest.mark.smoke
    @allure.story("Аутентификация пользователя")
    @allure.title("Вход зарегистрированного пользователя")
    @allure.description("Проверка успешного входа и получения непустого access token.")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_login_user(self, api_manager: ApiManager, registered_user):
        response = api_manager.auth_api.login_user(
            registered_user.email,
            registered_user.password
        )
        assert response.status_code == 200, "Пользователь не найден"

        login_user_response = LoginUserResponse.model_validate(response.json())
        assert login_user_response.accessToken != "", "Токен не должен быть пустым"
