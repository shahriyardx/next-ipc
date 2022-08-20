import json

from websockets.server import serve

from .models import IPCResponse


class IPCServer:
    ROUTES = {}

    def __init__(
        self,
        bot,
        host: str = "localhost",
        port: int = 9876,
        secret_key: str = None,
    ):
        self.bot = bot
        self.host = host
        self.port = port
        self.loop = bot.loop
        self._endpoints = {}
        self._secret_key = secret_key

    def route(self, name=None):
        def decorator(func):
            if not name:
                self._endpoints[func.__name__] = func
            else:
                self._endpoints[name] = func

            return func

        return decorator

    def update_endpoints(self):
        self._endpoints = {**self._endpoints, **self.ROUTES}
        self.ROUTES = {}

    async def process_data(self, message: str):
        try:
            return json.loads(message)
        except Exception:
            return None

    async def send_response(self, websocket, data):
        await websocket.send(json.dumps({"data": data}))

    async def send_error(self, websocket, message, code):
        data = json.dumps({"error": {"code": code, "message": message}})

        await websocket.send(data)

    async def handler(self, websocket, path):
        self.update_endpoints()

        async for message in websocket:
            data = await self.process_data(message)

            if not data:
                await self.send_error(websocket, "invalid request", 400)
                continue

            response = IPCResponse(data)
            endpoint = response.endpoint
            headers = response.headers

            if self._secret_key and self._secret_key != headers.Authorization:
                await self.send_error(websocket, "invalid secret key", 403)
                continue

            if endpoint not in self._endpoints:
                await self.send_error(websocket, f"invalid endpoint '{endpoint}'", 404)
                continue

            try:
                attempted_cls = self.bot.cogs.get(
                    self._endpoints[endpoint].__qualname__.split(".")[0]
                )

                if attempted_cls:
                    arguments = (attempted_cls, response)
                else:
                    arguments = (response,)
            except AttributeError:
                arguments = (response,)

            try:
                result = await self._endpoints[endpoint](*arguments)
                if result:
                    await self.send_response(websocket, result)
                else:
                    await self.send_response(websocket, None)
            except Exception as error:
                await self.send_error(
                    websocket,
                    f"internal server error. Type: {type(error).__name__}",
                    500,
                )

    def start(self):
        server = serve(self.handler, self.host, self.port)
        self.bot.loop.run_until_complete(server)


def route(name=None):
    def decorator(func):
        if not name:
            IPCServer.ROUTES[func.__name__] = func
        else:
            IPCServer.ROUTES[name] = func

        return func

    return decorator
