from discord.ext.commands import Cog, command, CommandError
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
        url = "https://api.waifu.pics/sfw/waifu"
        try:
            response = requests.get(url)
            base_json = response.json()
        except Exception as ex:
            print(f"err {ex}")
            raise CommandError(f"Something went wrong, try again leter")

        try:
            url_pic = base_json["url"]
            async with aiohttp.ClientSession() as session:
                async with session.get(url_pic) as resp:
                    if resp.status != 200:
                        print(f"resp not 200 {resp}")
                        pass
                    else:
                        filename = f"./temp/anime-waifu-{ctx.author.id}"
                        file = await aiofiles.open(f"{filename}_temp", mode="wb")
                        await file.write(await resp.read())
                        await file.close()

                        im = Image.open(f"{filename}_temp")
                        rgb_im = im.convert("RGB")
                        rgb_im.save(f"{filename}.jpg")

                        await ctx.send(file=File(f"{filename}.jpg"))

                        if os.path.isfile(f"{filename}.jpg"):
                            os.remove(f"{filename}.jpg")
                        if os.path.isfile(f"{filename}_temp"):
                            os.remove(f"{filename}_temp")
        except Exception as ex:
            print(f"err {ex}")
            raise CommandError(f"Something went wrong, try again leter")

    @Cog.listener()
    async def on_ready(self):
        if not self.bot.ready:
            self.bot.cogs_ready.ready_up("command_anime")


def setup(bot):
    bot.add_cog(Anime(bot))
