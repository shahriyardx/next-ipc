from quart import Quart

from next_ipc.client import IPCClient

app = Quart(__name__)
ipc = IPCClient(secret_key="test")


@app.get("/")
async def index():
    return await ipc.request("get_user", user_id=696939596667158579)


app.run()
