import json

import async_timeout
from websockets.client import connect


class IPCClient:
    ROUTES = {}

    def __init__(
        self,
        host: str = "localhost",
        port: int = 9876,
        secret_key: str = None,
        ssl: bool = False,
    ):
        self.ssl = ssl
        self.host = host
        self.port = port
        self._secret_key = secret_key

    async def request(self, endpoint, **kwargs):
        payload = {
            "endpoint": endpoint,
            "headers": {"Authorization": self._secret_key},
            "data": kwargs,
        }

        async with async_timeout.timeout(10):
            async with connect(
                f"{'wss' if self.ssl else 'ws'}://{self.host}:{self.port}"
            ) as con:
                await con.send(json.dumps(payload))

                message = await con.recv()
                try:
                    data = json.loads(message)
                    return data
                except:
                    return message
