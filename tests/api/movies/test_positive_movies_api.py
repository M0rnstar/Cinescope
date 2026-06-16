import pytest
from api.api_manager import ApiManager
from conftest import movie_with_string_price


class TestPositiveMoviesApi:
    def test_get_all_movies(self, api_manager: ApiManager):
        response = api_manager.movies_api.get_all_movies()

        assert response.status_code == 200, "Ошибка запроса"
        json_data = response.json()
        assert "movies" in json_data, "Нет поля фильмов в ответе сервера"
        assert isinstance(json_data["movies"], list), "Поле movies должно быть списком"
        assert len(json_data["movies"]) > 0, "Список фильмов пуст"
        assert "name" in json_data["movies"][0], "Нет имени фильма внутри списка"

    def test_get_all_movies_with_genre_id(self, api_manager: ApiManager):
        response = api_manager.movies_api.get_all_movies(genreId=1)

        assert response.status_code == 200, "Ошибка запроса"
        json_data = response.json()
        movies = json_data["movies"]

        assert len(movies) != 0, "Список фильмов пуст"
        assert all(movie["genreId"] == 1 for movie in movies)

    @pytest.mark.parametrize("min_price, max_price", [
        (1, 50),
        (100, 500),
        (501, 1000)
    ])
    def test_get_all_movies_with_price(self, api_manager: ApiManager, min_price: int, max_price: int):
        response = api_manager.movies_api.get_all_movies(minPrice=min_price, maxPrice=max_price)

        assert response.status_code == 200, "Неправильные параметры"
        json_data = response.json()
        movies = json_data["movies"]

        assert len(movies) != 0, "Список фильмов пуст"
        assert all(min_price <= movie["price"] <= max_price for movie in movies)

    def test_create_movie(self, super_admin, test_movie):
        response = super_admin.api.movies_api.create_movie(test_movie)

        assert response.status_code == 201, "Ошибка создания фильма"
        json_data = response.json()
        assert "id" in json_data, "У фильма нет ID"
        assert "name" in json_data, "Нет имени фильма внутри ответа"
        assert "genre" in json_data, "У фильма отутствует поле жанра"
        assert isinstance(json_data["genre"], dict)
        assert "name" in json_data["genre"]
        assert json_data["name"] == test_movie["name"], "Имя фильма не совпадает с отправленным"
        assert json_data["price"] == test_movie["price"], "Стоимость фильма не совпадает с отправленным"
        assert json_data["description"] == test_movie["description"], "Описание фильма не совпадает с отправленным"

        assert "price" in json_data, "Нет стоимости фильма"
        movie_price = json_data["price"]
        assert isinstance(movie_price, int), "Стоимость фильма не является целым числом"

    def test_get_movie_by_id(self, api_manager: ApiManager, movie_id):
        response = api_manager.movies_api.get_movie_by_id(movie_id)

        assert response.status_code == 200, "Не удалось получить фильм по ID"

        json_data = response.json()
        assert json_data["id"] == movie_id, "ID не совпадают"
        assert "name" in json_data, "Нет имени фильма внутри ответа"
        assert "description" in json_data, "Нет описания фильма внутри ответа"
        assert "genre" in json_data, "У фильма отутствует поле жанра"
        assert isinstance(json_data["genre"], dict)
        assert "name" in json_data["genre"]

        assert "price" in json_data, "Нет стоимости фильма"
        movie_price = json_data["price"]
        assert isinstance(movie_price, int), "Стоимость фильма не является целым числом"

    def test_delete_movie(self, movie_id, super_admin):
        delete_response = super_admin.api.movies_api.delete_movie(movie_id)
        assert delete_response.status_code == 200, "Ошибка при удалении фильма"

        get_response = super_admin.api.movies_api.get_movie_by_id(movie_id)
        assert get_response.status_code == 404, "Фильм не удалился"

    def test_update_movie(self, test_movie, movie_id, super_admin):
        update_response = super_admin.api.movies_api.update_movie(test_movie, movie_id)
        assert update_response.status_code == 200, "Ошибка обновления данных фильма"

        get_response = super_admin.api.movies_api.get_movie_by_id(movie_id)
        assert get_response.status_code == 200, "Фильм не найден"
        updated_data = get_response.json()

        assert test_movie["name"] == updated_data["name"], "Имя фильма не обновилась"
        assert test_movie["price"] == updated_data["price"], "Стоимость фильма не обновилась"
        assert test_movie["description"] == updated_data["description"], "Описание фильма не обновилось"
