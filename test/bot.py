import os

from nextcord import Intents, User
from nextcord.ext import commands
from dotenv import load_dotenv

from next_ipc import IPCServer
from next_ipc.server import route

load_dotenv(".env")


class Cog(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot

    @route()
    async def get_user(self, data):
        user: User = await self.bot.fetch_user(data.user_id)
        return user._to_minimal_user_json()


class CCV2(commands.AutoShardedBot):
    def __init__(self, **options) -> None:
        super().__init__(**options)

    async def on_ready(self):
        print("Ready")


intents = Intents.default()
intents.message_content = True

bot = CCV2(command_prefix="t", intents=intents)
bot.ipc_server = IPCServer(bot, secret_key="test")
bot.ipc_server.start()
bot.add_cog(Cog(bot))

bot.run(os.getenv("TOKEN"))
