from discord.ext.commands import Cog, command
from discord import Message, File
import aiohttp
import aiofiles
import asyncio
import os
from PIL import Image
from derpibooru import Search, sort


class Pony(Cog):
    def __init__(self, bot) -> None:
        super().__init__()
        self.bot = bot

    @command(name="pony", help="Show random pony images")
    async def pony(self, ctx: Message):
        for img in Search().sort_by(sort.RANDOM).limit(1):
            try:
                async with aiohttp.ClientSession() as session:
                    async with session.get(img.full) as resp:
                        if resp.status != 200:
                            print(f"resp not 200 {resp}")
                            pass
                        else:
                            filename = f"./temp/pony-{ctx.author.id}"
                            file = await aiofiles.open(f"{filename}_temp", mode="wb")
                            await file.write(await resp.read())
                            await file.close()

                            im = Image.open(f"{filename}_temp")
                            rgb_im = im.convert("RGB")
                            rgb_im.save(f"{filename}.jpg")

                            await ctx.reply(f"Source: [Go To]({img.url})")
                            await ctx.send(file=File(f"{filename}.jpg"))

                            if os.path.isfile(f"{filename}.jpg"):
                                os.remove(f"{filename}.jpg")
                            if os.path.isfile(f"{filename}_temp"):
                                os.remove(f"{filename}_temp")
            except Exception as ex:
                print(f"err {ex}")
                await ctx.reply(f"Something went wrong, try again leter")
                pass

    @command(name="ponywall", help="Show random pony wallpaper images")
    async def ponywall(self, ctx: Message):
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
            self.bot.cogs_ready.ready_up("command_pony")


def setup(bot):
    bot.add_cog(Pony(bot))
