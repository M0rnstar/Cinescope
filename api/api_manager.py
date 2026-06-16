from api.auth_api import AuthApi
from api.movies_api import MoviesApi
from api.user_api import UserApi


class ApiManager:
    def __init__(self, session):
        self.session = session
        self.auth_api = AuthApi(session)
        self.movies_api = MoviesApi(session)
        self.user_api = UserApi(session)

    def close_session(self):
        self.session.close()