import allure
import pytest

from models.user_data import RegisterUserResponse


@pytest.mark.api
@pytest.mark.regression
@allure.epic("Cinescope API")
@allure.feature("Пользователи")
class TestUser:
    @pytest.mark.smoke
    @allure.story("Создание пользователя")
    @allure.title("Создание пользователя супер-администратором")
    @allure.description("Проверка успешного создания пользователя и соответствия данных в ответе запросу.")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_create_user(self, super_admin, creation_user_data):
        response = super_admin.api.user_api.create_user(creation_user_data)
        assert response.status_code == 201, response.text

        created_user_response = RegisterUserResponse.model_validate(response.json())
        assert created_user_response.id != '', "ID должен быть не пустым"
        assert created_user_response.email == creation_user_data.email
        assert created_user_response.fullName == creation_user_data.fullName
        assert created_user_response.roles == creation_user_data.roles
        assert created_user_response.verified is True

    @pytest.mark.smoke
    @allure.story("Получение пользователя")
    @allure.title("Получение пользователя по ID и email")
    @allure.description("Проверка, что поиск пользователя по ID и email возвращает одинаковые данные.")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_get_user_by_locator(self, super_admin, creation_user_data):
        with allure.step("Создать пользователя"):
            created_user_response = super_admin.api.user_api.create_user(creation_user_data)
            assert created_user_response.status_code == 201, created_user_response.text

            created_user_response = RegisterUserResponse.model_validate(created_user_response.json())

        with allure.step("Получить пользователя по ID"):
            response_by_id = super_admin.api.user_api.get_user(created_user_response.id)
            assert response_by_id.status_code == 200, response_by_id.text
            user_by_id = RegisterUserResponse.model_validate(response_by_id.json())

        with allure.step("Получить пользователя по email"):
            response_by_email = super_admin.api.user_api.get_user(creation_user_data.email)
            assert response_by_email.status_code == 200, response_by_email.text
            user_by_email = RegisterUserResponse.model_validate(response_by_email.json())

        with allure.step("Сравнить данные пользователя"):
            assert user_by_id == user_by_email, "Содержание ответов должно быть идентичным"
            assert user_by_id.id != '', "ID должен быть не пустым"
            assert user_by_id.email == creation_user_data.email
            assert user_by_id.fullName == creation_user_data.fullName
            assert user_by_id.roles == creation_user_data.roles
            assert user_by_id.verified is True

    @pytest.mark.slow
    @allure.story("Получение пользователя")
    @allure.title("Запрет получения пользователя для роли USER")
    @allure.description("Проверка запрета получения пользователя по email без административной роли.")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_get_user_by_id_common_user(self, common_user):
        response = common_user.api.user_api.get_user(common_user.email)

        assert response.status_code == 403

