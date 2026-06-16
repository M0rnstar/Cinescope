from api.api_manager import ApiManager


class TestNegativeMoviesApi:
    # Тесты для GET /movies
    def test_negative_page(self, api_manager: ApiManager):
        response = api_manager.movies_api.get_all_movies(page=-1)
        assert response.status_code == 400, "Отрицательная страница не обрабатывается"

    def test_negative_page_size(self, api_manager: ApiManager):
        response = api_manager.movies_api.get_all_movies(pageSize=-20)
        assert response.status_code == 400, "Отрицательный размер страницы не обрабатывается"

    # Тесты для POST /movies
    def test_create_movie_with_existing_name(self, super_admin, movie_with_existing_name):
        response = super_admin.api.movies_api.create_movie(movie_with_existing_name)
        assert response.status_code == 409, "Не вызывается ошибка при создании фильма с таким же именем"

    def test_create_movie_with_user_rules(self, common_user, test_movie):
        response = common_user.api.movies_api.create_movie(test_movie)
        assert response.status_code == 403, "Обычный пользователь смог создать фильм"

    def test_create_movie_with_negative_price(self, super_admin, movie_with_string_price):
        response = super_admin.api.movies_api.create_movie(movie_with_string_price)
        assert response.status_code == 400, "Неверная обработка ошибки"

    def test_create_movie_with_empty_body(self, super_admin):
        response = super_admin.api.movies_api.create_movie({})
        assert response.status_code == 400, "Создание фильма с пустым телом не вызывает ошибку"

    # Тесты для GET /movies/{id}
    def test_get_movie_by_string_id(self, api_manager: ApiManager):
        response = api_manager.movies_api.get_movie_by_id("1")
        assert response.status_code == 404, "Нет обработки id на число"

    def test_get_movie_by_negative_id(self, api_manager: ApiManager):
        response = api_manager.movies_api.get_movie_by_id(-1)
        assert response.status_code == 404, "Не вызывается ошибка при отрицательном id"

    def test_get_movie_by_non_existing_id(self, api_manager: ApiManager):
        response = api_manager.movies_api.get_movie_by_id(99999999)
        assert response.status_code == 404, "Не вызывается 404 при несуществующем id"

    # Тесты для DELETE /movies/{id}
    def test_delete_movie_by_string_id(self, super_admin):
        response = super_admin.api.movies_api.delete_movie("1")
        assert response.status_code == 404, "Нет обработки id на число"

    def test_delete_movie_by_negative_id(self, super_admin):
        response = super_admin.api.movies_api.delete_movie(-1)
        assert response.status_code == 404, "Не вызывается ошибка при отрицательном id"

    def test_delete_movie_by_non_existing_id(self, super_admin):
        response = super_admin.api.movies_api.delete_movie(9999999999)
        assert response.status_code == 404, "Не вызывается 404 при несуществующем id"

    # Тесты для PATCH /movies/{id}
    def test_update_movie_by_non_existing_id(self, super_admin, test_movie):
        response = super_admin.api.movies_api.update_movie(test_movie, 99999999999)
        assert response.status_code == 404, "Не вызывается 404 при несуществующем id"

    def test_update_movie_with_string_price(self, super_admin, movie_id, movie_with_string_price):
        response = super_admin.api.movies_api.update_movie(movie_with_string_price, movie_id)
        assert response.status_code == 400, "Нет валидации price на проверку целочисленности"
