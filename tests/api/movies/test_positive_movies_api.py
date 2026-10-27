import datetime
import pytest
import allure
from api.api_manager import ApiManager
from conftest import movie_with_string_price
from db_models.movies import MovieDBModel
from models.movie_data import MovieDetailsResponse, MovieResponse, MoviesResponse


@pytest.mark.api
@pytest.mark.regression
@allure.epic("Cinescope API")
@allure.feature("Фильмы")
class TestPositiveMoviesApi:
    @pytest.mark.smoke
    @allure.story("Получение списка фильмов")
    @allure.title("Получение списка фильмов без фильтров")
    @allure.description("Проверка успешного получения непустого списка фильмов.")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_get_all_movies(self, api_manager: ApiManager):
        response = api_manager.movies_api.get_all_movies()

        assert response.status_code == 200, "Ошибка запроса"
        movies_response = MoviesResponse.model_validate(response.json())
        assert movies_response.movies, "Список фильмов пуст"

    @allure.story("Получение списка фильмов")
    @allure.title("Фильтрация фильмов по жанру")
    @allure.description("Проверка, что API возвращает фильмы только указанного жанра.")
    @allure.severity(allure.severity_level.NORMAL)
    def test_get_all_movies_with_genre_id(self, api_manager: ApiManager):
        response = api_manager.movies_api.get_all_movies(genreId=8)

        assert response.status_code == 200, "Ошибка запроса"
        movies_response = MoviesResponse.model_validate(response.json())

        assert movies_response.movies, "Список фильмов пуст"
        assert all(movie.genreId == 8 for movie in movies_response.movies)

    @pytest.mark.parametrize("min_price, max_price", [
        (1, 50),
        (100, 500),
        (501, 1000)
    ])
    @allure.story("Получение списка фильмов")
    @allure.title("Фильтрация фильмов по цене от {min_price} до {max_price}")
    @allure.description("Проверка фильтрации списка фильмов по заданному диапазону цен.")
    @allure.severity(allure.severity_level.NORMAL)
    def test_get_all_movies_with_price(self, api_manager: ApiManager, min_price: int, max_price: int):
        response = api_manager.movies_api.get_all_movies(minPrice=min_price, maxPrice=max_price)

        assert response.status_code == 200, "Неправильные параметры"
        movies_response = MoviesResponse.model_validate(response.json())

        assert movies_response.movies, "Список фильмов пуст"
        assert all(min_price <= movie.price <= max_price for movie in movies_response.movies)

    @allure.story("Получение фильма по ID")
    @allure.title("Получение существующего фильма по ID")
    @allure.description("Проверка успешного получения фильма и обязательных полей ответа.")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_get_movie_by_id(self, api_manager: ApiManager, movie_id):
        response = api_manager.movies_api.get_movie_by_id(movie_id)

        assert response.status_code == 200, "Не удалось получить фильм по ID"

        movie_response = MovieDetailsResponse.model_validate(response.json())
        assert movie_response.id == movie_id, "ID не совпадают"

    @pytest.mark.smoke
    @allure.story("Создание фильма")
    @allure.title("Создание фильма с валидными данными")
    @allure.description("Проверка успешного создания фильма и соответствия данных в ответе запросу.")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_create_movie(self, super_admin, test_movie):
        response = super_admin.api.movies_api.create_movie(test_movie)

        assert response.status_code == 201, "Ошибка создания фильма"
        movie_response = MovieResponse.model_validate(response.json())
        assert movie_response.name == test_movie["name"], "Имя фильма не совпадает с отправленным"
        assert movie_response.price == test_movie["price"], "Стоимость фильма не совпадает с отправленным"
        assert movie_response.description == test_movie["description"], "Описание фильма не совпадает с отправленным"

    @pytest.mark.slow
    @allure.story("Сохранение фильма в БД")
    @allure.title("Сохранение созданного через API фильма в БД")
    @allure.description("Проверка появления фильма в БД после создания через API и удаления записи после запроса на удаление.")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_create_and_delete_movie_in_db(self, super_admin, test_movie, db_helper, db_session):
        with allure.step("Проверить отсутствие фильма в БД"):
            movie_before_creation = db_helper.get_movie_by_name(test_movie["name"])
            assert movie_before_creation is None, "Фильм уже есть в БД до начала теста"

        with allure.step("Создать фильм через API"):
            create_response = super_admin.api.movies_api.create_movie(test_movie)
            assert create_response.status_code == 201, "Ошибка создания фильма"

            created_movie = MovieResponse.model_validate(create_response.json())
            created_movie_id = created_movie.id

        try:
            with allure.step("Проверить данные созданного фильма в БД"):
                db_session.expire_all()
                movie_from_db = db_helper.get_movie_by_id(created_movie_id)
                assert movie_from_db is not None, "Фильм не появился в БД после создания через API"
                assert movie_from_db.name == test_movie["name"], "Название фильма в БД не совпадает"
                assert movie_from_db.price == test_movie["price"], "Цена фильма в БД не совпадает"
                assert movie_from_db.description == test_movie["description"], "Описание фильма в БД не совпадает"

            with allure.step("Удалить фильм и проверить его отсутствие в БД"):
                delete_response = super_admin.api.movies_api.delete_movie(created_movie_id)
                assert delete_response.status_code == 200, "Ошибка удаления фильма через API"
                MovieDetailsResponse.model_validate(delete_response.json())

                db_session.expire_all()
                deleted_movie_from_db = db_helper.get_movie_by_id(created_movie_id)
                assert deleted_movie_from_db is None, "Фильм остался в БД после удаления через API"
        finally:
            db_session.expire_all()
            if db_helper.get_movie_by_id(created_movie_id):
                super_admin.api.movies_api.delete_movie(created_movie_id)

    @pytest.mark.smoke
    @allure.story("Удаление фильма")
    @allure.title("Удаление существующего фильма")
    @allure.description("Проверка удаления фильма из БД и недоступности фильма по ID после удаления.")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_delete_movie(self, movie_id, super_admin, test_movie, db_helper, db_session):
        with allure.step("Подготовить существующий фильм в БД"):
            movie_from_db = db_helper.get_movie_by_id(movie_id)

            if movie_from_db is None:
                movie_from_db = MovieDBModel(
                    id=movie_id,
                    name=test_movie["name"],
                    price=test_movie["price"],
                    description=test_movie["description"],
                    image_url=test_movie["imageUrl"],
                    location=test_movie["location"],
                    published=test_movie["published"],
                    genre_id=test_movie["genreId"],
                    created_at=datetime.datetime.now(),
                    rating=0
                )
                db_session.add(movie_from_db)
                db_session.commit()

            assert db_helper.get_movie_by_id(movie_id) is not None, "Фильма нет в БД до удаления"

        with allure.step("Удалить фильм через API"):
            delete_response = super_admin.api.movies_api.delete_movie(movie_id)
            assert delete_response.status_code == 200, "Ошибка при удалении фильма"
            MovieDetailsResponse.model_validate(delete_response.json())

        with allure.step("Проверить отсутствие фильма в БД и API"):
            db_session.expire_all()
            deleted_movie_from_db = db_helper.get_movie_by_id(movie_id)
            assert deleted_movie_from_db is None, "Фильм остался в БД после удаления"

            get_response = super_admin.api.movies_api.get_movie_by_id(movie_id)
            assert get_response.status_code == 404, "Фильм не удалился"

    @pytest.mark.smoke
    @allure.story("Обновление фильма")
    @allure.title("Обновление существующего фильма")
    @allure.description("Проверка изменения данных фильма и получения обновлённых значений по ID.")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_update_movie(self, test_movie, movie_id, super_admin):
        with allure.step("Обновить данные фильма"):
            update_response = super_admin.api.movies_api.update_movie(test_movie, movie_id)
            assert update_response.status_code == 200, "Ошибка обновления данных фильма"
            MovieResponse.model_validate(update_response.json())

        with allure.step("Получить фильм и проверить обновлённые данные"):
            get_response = super_admin.api.movies_api.get_movie_by_id(movie_id)
            assert get_response.status_code == 200, "Фильм не найден"
            updated_movie = MovieDetailsResponse.model_validate(get_response.json())

            assert test_movie["name"] == updated_movie.name, "Имя фильма не обновилась"
            assert test_movie["price"] == updated_movie.price, "Стоимость фильма не обновилась"
            assert test_movie["description"] == updated_movie.description, "Описание фильма не обновилось"
