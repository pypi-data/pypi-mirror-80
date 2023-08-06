from retry import retry

import requests

from lol_esports_parser.config import endpoints, MAX_RETRIES, RETRY_DELAY, config
from lol_esports_parser.logger import lol_esports_parser_logger


@retry(tries=MAX_RETRIES, delay=RETRY_DELAY)
def get_id_token() -> str:
    session = requests.Session()

    # Get some basic identification cookies for the next request
    session.get("https://login.riotgames.com/")

    # Get the URI for the OAUTH flow
    response_put = session.put(
        "https://auth.riotgames.com/api/v1/authorization",
        json={"type": "auth", "username": config.riot_username, "password": config.riot_password},
    )

    # Write the id_token in our cookies
    session.get(response_put.json()["response"]["parameters"]["uri"])
    session.close()

    # Writing the token
    return session.cookies["id_token"]


class ACS:
    """Class handling connecting and retrieving games from ACS endpoints.
    """

    base_url = endpoints["acs"]["game"]

    def __init__(self):
        # TODO Cache the id token somewhere just in case? Not sure it’s needed
        self.id_token = get_id_token()

    @retry(tries=MAX_RETRIES, delay=RETRY_DELAY)
    def _get_from_api(self, uri):
        request_url = f"{self.base_url}{uri}"
        lol_esports_parser_logger.debug(f"Making a call to: {request_url}")

        response = requests.get(request_url, cookies={"id_token": self.id_token})

        if response.status_code != 200:
            lol_esports_parser_logger.error(f"Status code {response.status_code}")
            lol_esports_parser_logger.error(f"Headers: {response.headers}")
            lol_esports_parser_logger.error(f"Resp: {response.text}")
            raise requests.HTTPError

        return response.json()

    def get_game(self, server, game_id, game_hash):
        return self._get_from_api(f"{server}/{game_id}?gameHash={game_hash}")

    def get_game_timeline(self, server, game_id, game_hash):
        return self._get_from_api(f"{server}/{game_id}/timeline?gameHash={game_hash}")
