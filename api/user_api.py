from custom_requester.custom_requester import CustomRequester
from constants.endpoints import Endpoints
from constants.urls import Urls


class UserApi(CustomRequester):
    def __init__(self, session):
        self.session = session
        super().__init__(session=session, base_url=Urls.USER_BASE_URL.value)

    def get_user(self, user_locator):
        return self.send_request("GET", f"{Endpoints.USER.value}/{user_locator}")

    def create_user(self, user_data):
        return self.send_request(
            method="POST",
            endpoint=Endpoints.USER.value,
            json=user_data,
        )
