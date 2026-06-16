from constants.endpoints import Endpoints
from constants.urls import Urls
from custom_requester.custom_requester import CustomRequester


class AuthApi(CustomRequester):
    def __init__(self, session):
        super().__init__(session=session, base_url=Urls.AUTH_BASE_URL.value)

    def register_user(self, user_data):
        return self.send_request(
            method="POST",
            endpoint=Endpoints.REGISTER.value,
            json=user_data
            )

    def login_user(self, email, password):
        return self.send_request(
            method="POST",
            endpoint=Endpoints.LOGIN.value,
            json={
                "email": email,
                "password": password
            }
        )
