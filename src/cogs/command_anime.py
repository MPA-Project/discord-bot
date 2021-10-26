from discord.ext.commands import Cog, command
from discord import Message, File
from PIL import Image
import requests
import aiohttp
import aiofiles
import os


class Anime(Cog):
    def __init__(self, bot) -> None:
        super().__init__()
        self.bot = bot

    @command(name="anim", help="Show random anime images")
    async def anime(self, ctx: Message):
        await ctx.reply(f"Still working on progress...")

    @command(name="waifu", help="Show random waifu images")
    async def waifu(self, ctx: Message):
        # try:
        #     response = requests.get(
        #         "https://www.mylittlewallpaper.com/c/my-little-pony/api/v1/random.json?limit=1"
        #     )
        #     base_json = response.json()
        # except:
        #     pass

        await ctx.reply(f"Still working on progress...")

    @Cog.listener()
    async def on_ready(self):
        if not self.bot.ready:
            self.bot.cogs_ready.ready_up("command_anime")


def setup(bot):
    bot.add_cog(Anime(bot))
