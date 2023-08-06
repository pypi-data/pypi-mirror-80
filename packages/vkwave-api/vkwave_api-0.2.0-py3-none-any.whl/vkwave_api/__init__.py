from vkwave.client import AIOHTTPClient
from vkwave.api import API as LibAPI
from vkwave.api.token import Token
from vkwave.api.token.token import UserSyncSingleToken
from vkwave.api import APIOptionsRequestContext


class API:
    def __init__(self, token: str):
        client = AIOHTTPClient()
        token = UserSyncSingleToken(Token(token))
        self._api = LibAPI(tokens=token, clients=client)

    def get_api(self) -> APIOptionsRequestContext:
        return self._api.get_context()

    async def close(self) -> None:
        await self._api.default_api_options.clients[0].close()

def run(f):
    import asyncio
    loop = asyncio.get_event_loop()
    loop.run_until_complete(f)
