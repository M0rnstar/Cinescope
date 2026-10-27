from api.api_manager import ApiManager
from entities.user import User
import pytest
import allure


@pytest.mark.api
@pytest.mark.regression
@allure.epic("Cinescope API")
@allure.feature("Фильмы")
class TestNegativeMoviesApi:
    # Тесты для GET /movies
    @allure.story("Получение списка фильмов")
    @allure.title("Запрос списка фильмов с отрицательным номером страницы")
    @allure.description("Проверка отклонения запроса с отрицательным значением параметра page.")
    @allure.severity(allure.severity_level.NORMAL)
    def test_negative_page(self, api_manager: ApiManager):
        response = api_manager.movies_api.get_all_movies(page=-1)
        assert response.status_code == 400, "Отрицательная страница не обрабатывается"

    @allure.story("Получение списка фильмов")
    @allure.title("Запрос списка фильмов с отрицательным размером страницы")
    @allure.description("Проверка отклонения запроса с отрицательным значением параметра pageSize.")
    @allure.severity(allure.severity_level.NORMAL)
    def test_negative_page_size(self, api_manager: ApiManager):
        response = api_manager.movies_api.get_all_movies(pageSize=-20)
        assert response.status_code == 400, "Отрицательный размер страницы не обрабатывается"

    # Тесты для POST /movies
    @allure.story("Создание фильма")
    @allure.title("Создание фильма с уже существующим названием")
    @allure.description("Проверка запрета создания второго фильма с таким же названием.")
    @allure.severity(allure.severity_level.NORMAL)
    def test_create_movie_with_existing_name(self, super_admin, movie_with_existing_name):
        response = super_admin.api.movies_api.create_movie(movie_with_existing_name)
        assert response.status_code == 409, "Не вызывается ошибка при создании фильма с таким же именем"

    @pytest.mark.slow
    @pytest.mark.parametrize("roles", ["common_user", "admin"], indirect=True)
    @allure.story("Создание фильма")
    @allure.title("Запрет создания фильма для роли {roles}")
    @allure.description("Проверка, что создать фильм может только пользователь с ролью SUPER_ADMIN.")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_create_movie_with_another_roles(self, roles: User, test_movie):
        response = roles.api.movies_api.create_movie(test_movie)
        assert response.status_code == 403, "Фильм создан не суперадмином"

    @allure.story("Создание фильма")
    @allure.title("Создание фильма со строковым значением цены")
    @allure.description("Проверка отклонения запроса, в котором цена фильма не является числом.")
    @allure.severity(allure.severity_level.NORMAL)
    def test_create_movie_with_negative_price(self, super_admin, movie_with_string_price):
        response = super_admin.api.movies_api.create_movie(movie_with_string_price)
        assert response.status_code == 400, "Неверная обработка ошибки"

    @allure.story("Создание фильма")
    @allure.title("Создание фильма с пустым телом запроса")
    @allure.description("Проверка отклонения запроса без обязательных данных фильма.")
    @allure.severity(allure.severity_level.NORMAL)
    def test_create_movie_with_empty_body(self, super_admin):
        response = super_admin.api.movies_api.create_movie({})
        assert response.status_code == 400, "Создание фильма с пустым телом не вызывает ошибку"

    # Тесты для GET /movies/{id}
    @allure.story("Получение фильма по ID")
    @allure.title("Получение фильма со строковым ID")
    @allure.description("Проверка ответа API при передаче строки вместо числового идентификатора фильма.")
    @allure.severity(allure.severity_level.NORMAL)
    def test_get_movie_by_string_id(self, api_manager: ApiManager):
        response = api_manager.movies_api.get_movie_by_id("1")
        assert response.status_code == 404, "Нет обработки id на число"

    @allure.story("Получение фильма по ID")
    @allure.title("Получение фильма с отрицательным ID")
    @allure.description("Проверка ответа API при передаче отрицательного идентификатора фильма.")
    @allure.severity(allure.severity_level.NORMAL)
    def test_get_movie_by_negative_id(self, api_manager: ApiManager):
        response = api_manager.movies_api.get_movie_by_id(-1)
        assert response.status_code == 404, "Не вызывается ошибка при отрицательном id"

    @allure.story("Получение фильма по ID")
    @allure.title("Получение фильма по несуществующему ID")
    @allure.description("Проверка ответа API при запросе отсутствующего фильма.")
    @allure.severity(allure.severity_level.NORMAL)
    def test_get_movie_by_non_existing_id(self, api_manager: ApiManager):
        response = api_manager.movies_api.get_movie_by_id(99999999)
        assert response.status_code == 404, "Не вызывается 404 при несуществующем id"

    # Тесты для DELETE /movies/{id}
    @allure.story("Удаление фильма")
    @allure.title("Удаление фильма со строковым ID")
    @allure.description("Проверка ответа API при удалении фильма со строковым идентификатором.")
    @allure.severity(allure.severity_level.NORMAL)
    def test_delete_movie_by_string_id(self, super_admin):
        response = super_admin.api.movies_api.delete_movie("1")
        assert response.status_code == 404, "Нет обработки id на число"

    @allure.story("Удаление фильма")
    @allure.title("Удаление фильма с отрицательным ID")
    @allure.description("Проверка ответа API при удалении фильма с отрицательным идентификатором.")
    @allure.severity(allure.severity_level.NORMAL)
    def test_delete_movie_by_negative_id(self, super_admin):
        response = super_admin.api.movies_api.delete_movie(-1)
        assert response.status_code == 404, "Не вызывается ошибка при отрицательном id"

    @allure.story("Удаление фильма")
    @allure.title("Удаление фильма по несуществующему ID")
    @allure.description("Проверка ответа API при удалении отсутствующего фильма.")
    @allure.severity(allure.severity_level.NORMAL)
    def test_delete_movie_by_non_existing_id(self, super_admin):
        response = super_admin.api.movies_api.delete_movie(9999999999)
        assert response.status_code == 404, "Не вызывается 404 при несуществующем id"

    @pytest.mark.slow
    @pytest.mark.parametrize("roles", ["common_user", "admin"], indirect=True)
    @allure.story("Удаление фильма")
    @allure.title("Запрет удаления фильма для роли {roles}")
    @allure.description("Проверка, что удалить фильм может только пользователь с ролью SUPER_ADMIN.")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_delete_movie_by_another_roles(self, roles: User, movie_id):
        response = roles.api.movies_api.delete_movie(movie_id)
        assert response.status_code == 403, "Фильм создан не суперадмином"

    # Тесты для PATCH /movies/{id}
    @allure.story("Обновление фильма")
    @allure.title("Обновление фильма по несуществующему ID")
    @allure.description("Проверка ответа API при попытке обновить отсутствующий фильм.")
    @allure.severity(allure.severity_level.NORMAL)
    def test_update_movie_by_non_existing_id(self, super_admin, test_movie):
        response = super_admin.api.movies_api.update_movie(test_movie, 99999999999)
        assert response.status_code == 404, "Не вызывается 404 при несуществующем id"

    @allure.story("Обновление фильма")
    @allure.title("Обновление фильма со строковым значением цены")
    @allure.description("Проверка отклонения запроса на обновление с некорректным типом цены.")
    @allure.severity(allure.severity_level.NORMAL)
    def test_update_movie_with_string_price(self, super_admin, movie_id, movie_with_string_price):
        response = super_admin.api.movies_api.update_movie(movie_with_string_price, movie_id)
        assert response.status_code == 400, "Нет валидации price на проверку целочисленности"
