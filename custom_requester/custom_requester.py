import json
import logging
import requests
from constants.headers import Headers


class CustomRequester:
    base_headers = {
        Headers.CONTENT_TYPE.value: Headers.APPLICATION_JSON.value,
        Headers.ACCEPT.value: Headers.APPLICATION_JSON.value
    }

    def __init__(self, session: requests.Session = None, base_url: str = None):
        self.session = session or requests.Session()
        self.base_url = base_url or "https://auth.dev-cinescope.coconutqa.ru"
        self.session.headers.update(self.base_headers)
        self.logger = logging.getLogger(__name__)

    def send_request(self, method: str, endpoint: str, need_logging: bool = True, **kwargs):
        url = f"{self.base_url}{endpoint}"
        response = self.session.request(method=method, url=url, **kwargs)

        if need_logging:
            self.log_request_and_response(response)

        return response

    def update_headers(self, **headers):
        self.session.headers.update(headers)

    def set_auth_token(self, token: str):
        self.session.headers.update({
            "Authorization": f"Bearer {token}"
        })

    def log_request_and_response(self, response: requests.Response):
        try:
            request = response.request

            self.logger.info("\n%s REQUEST %s", "=" * 40, "=" * 40)
            self.logger.info("\n%s %s", request.method, request.url)
            self.logger.info("Headers: %s", dict(request.headers))

            if request.body:
                body = request.body
                if isinstance(body, bytes):
                    body = body.decode("utf-8", errors="replace")
                self.logger.info("Body: %s", body)

            self.logger.info("\n%s RESPONSE %s", "=" * 40, "=" * 40)
            self.logger.info("\nStatus code: %s", response.status_code)

            try:
                formatted_json = json.dumps(response.json(), indent=4, ensure_ascii=False)
                self.logger.info("Response JSON:\n%s", formatted_json)
            except Exception:
                self.logger.info("Response text:\n%s", response.text)

        except Exception as e:
            self.logger.error("Logging failed: %s", e)
