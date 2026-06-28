import json
import logging
import os
import requests
from pydantic import BaseModel

from constants.headers import Headers


class CustomRequester:
    base_headers = {
        Headers.CONTENT_TYPE.value: Headers.APPLICATION_JSON.value,
        Headers.ACCEPT.value: Headers.APPLICATION_JSON.value
    }

    def __init__(self, session: requests.Session = None, base_url: str = None):
        self.session = session or requests.Session()
        self.base_url = base_url or "https://auth.dev-cinescope.coconutqa.ru"
        self.session.headers = self.base_headers.copy()
        self.logger = logging.getLogger(__name__)

    def send_request(self, method: str, endpoint: str, need_logging: bool = True, **data):
        url = f"{self.base_url}{endpoint}"
        if isinstance(data.get("json"), BaseModel):
            data["json"] = json.loads(data["json"].model_dump_json(exclude_unset=True))
        response = self.session.request(method=method, url=url, **data)

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

            headers = " \\\n".join(
                f"-H '{header}: {value}'"
                for header, value in request.headers.items()
            )
            full_test_name = os.environ.get("PYTEST_CURRENT_TEST", "").replace(" (call)", "")

            body = ""
            if request.body:
                request_body = request.body
                if isinstance(request_body, bytes):
                    request_body = request_body.decode("utf-8", errors="replace")

                try:
                    parsed_body = json.loads(request_body)
                    for field in ("password", "passwordRepeat"):
                        if field in parsed_body:
                            parsed_body[field] = "***"
                    request_body = json.dumps(parsed_body, ensure_ascii=False)
                except (TypeError, json.JSONDecodeError):
                    pass

                if request_body != "{}":
                    body = f"-d '{request_body}' \\\n"

            self.logger.info(
                "\npytest %s\n"
                "curl -X %s '%s' \\\n"
                "%s \\\n"
                "%s",
                full_test_name,
                request.method,
                request.url,
                headers,
                body,
            )

            if not response.ok:
                self.logger.info(
                    "\nRESPONSE:"
                    "\nSTATUS_CODE: %s"
                    "\nDATA: %s",
                    response.status_code,
                    response.text,
                )

        except Exception as e:
            self.logger.error("Logging failed: %s", e)
