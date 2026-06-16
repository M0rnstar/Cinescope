from constants.endpoints import Endpoints
from constants.urls import Urls
from custom_requester.custom_requester import CustomRequester


class MoviesApi(CustomRequester):
    def __init__(self, session):
        super().__init__(session=session, base_url=Urls.MOVIES_BASE_URL.value)

    def get_all_movies(self, **params):
        return self.send_request(
            method="GET",
            endpoint=Endpoints.MOVIES.value,
            params=params
        )

    def create_movie(self, movie_data):
        return self.send_request(
            method="POST",
            endpoint=Endpoints.MOVIES.value,
            json=movie_data
        )

    def get_movie_by_id(self, movie_id):
        return self.send_request(
            method="GET",
            endpoint=f"{Endpoints.MOVIES.value}/{movie_id}"
        )

    def delete_movie(self, movie_id):
        return self.send_request(
            method="DELETE",
            endpoint=f"{Endpoints.MOVIES.value}/{movie_id}"
        )

    def update_movie(self, movie_data, movie_id):
        return self.send_request(
            method="PATCH",
            endpoint=f"{Endpoints.MOVIES.value}/{movie_id}",
            json=movie_data
        )
