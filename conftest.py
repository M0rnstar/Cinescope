from models.user_data import UserData
import pytest
import requests
from api.api_manager import ApiManager
from utils.data_generator import DataGenerator
from entities.user import User
from resources.user_creds import SuperAdminCreds
from constants.roles import Roles


@pytest.fixture
def user_session():
    user_pool = []

    def _create_user_session():
        session = requests.Session()
        api_manager = ApiManager(session)
        user_pool.append(api_manager)
        return api_manager

    yield _create_user_session

    for user in user_pool:
        user.close_session()


@pytest.fixture(scope="session")
def session():
    http_session = requests.Session()
    yield http_session
    http_session.close()


@pytest.fixture(scope="session")
def api_manager(session):
    return ApiManager(session)


@pytest.fixture
def test_user() -> UserData:
    random_email = DataGenerator.generate_random_email()
    random_name = DataGenerator.generate_random_name()
    random_password = DataGenerator.generate_random_password()

    return UserData(
        email=random_email,
        fullName=random_name,
        password=random_password,
        passwordRepeat=random_password,
        roles=[Roles.USER]
    )



@pytest.fixture(scope="function")
def creation_user_data(test_user: UserData) -> UserData:
    return test_user.model_copy(
        update={
            "verified": True,
            "banned": False,
        }
    )


@pytest.fixture
def super_admin(user_session):
    new_session = user_session()

    super_admin = User(
        SuperAdminCreds.USERNAME, SuperAdminCreds.PASSWORD, [Roles.SUPER_ADMIN.value], new_session
    )

    response = super_admin.api.auth_api.login_user(*super_admin.creds)
    assert response.status_code == 201, response.text

    token = response.json().get("accessToken")
    assert token is not None, "Токен доступа отсутствует в ответе"

    super_admin.api.user_api.set_auth_token(token)
    return super_admin


@pytest.fixture
def admin(user_session, super_admin, creation_user_data):
    new_session = user_session()

    admin = User(
        creation_user_data.email,
        creation_user_data.password,
        [Roles.ADMIN.value],
        new_session
    )
    super_admin.api.user_api.create_user(creation_user_data)
    response = admin.api.auth_api.login_user(*admin.creds)
    assert response.status_code == 201

    token = response.json().get("accessToken")
    assert token is not None

    admin.api.user_api.set_auth_token(token)
    return admin


@pytest.fixture
def common_user(user_session, super_admin, creation_user_data):
    new_session = user_session()

    common_user = User(
        creation_user_data.email,
        creation_user_data.password,
        [Roles.USER.value],
        new_session
    )
    super_admin.api.user_api.create_user(creation_user_data)
    response = common_user.api.auth_api.login_user(*common_user.creds)
    assert response.status_code == 201, response.text

    token = response.json().get("accessToken")
    assert token is not None, "Токен доступа отсутствует в ответе"

    common_user.api.user_api.set_auth_token(token)
    return common_user


@pytest.fixture
def roles(request):
    return request.getfixturevalue(request.param)


@pytest.fixture
def registered_user(api_manager, test_user):
    auth_client = api_manager.auth_api
    response = auth_client.register_user(test_user)
    assert response.status_code == 201, response.text

    response_data = response.json()
    assert "id" in response_data, "Пользователь не был создан"

    return test_user


@pytest.fixture
def test_movie():
    return DataGenerator.generate_random_movie()


@pytest.fixture
def movie(super_admin, test_movie):
    movie_client = super_admin.api.movies_api
    response = movie_client.create_movie(test_movie)
    assert response.status_code == 201, "Ошибка создания фильма"

    movie_data = response.json()
    yield movie_data

    response = movie_client.get_movie_by_id(movie_data["id"])
    if response.status_code == 200:
        movie_client.delete_movie(movie_data["id"])


@pytest.fixture
def movie_with_existing_name(movie):
    return DataGenerator.generate_movie_with_existing_name(movie["name"])


@pytest.fixture
def movie_id(movie):
    return movie["id"]


@pytest.fixture
def movie_with_string_price():
    return DataGenerator.generate_movie_with_custom_price("Цена")
