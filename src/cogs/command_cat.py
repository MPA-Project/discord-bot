from discord.ext.commands import Cog, command
from discord import Message, File
from PIL import Image
import requests
import aiohttp
import aiofiles
import os


class Cat(Cog):
    def __init__(self, bot) -> None:
        super().__init__()
        self.bot = bot

    @command(
        name="cat",
        help="Show random cats",
    )
    async def cat(self, ctx: Message):
        try:
            response = requests.get("https://api.thecatapi.com/v1/images/search")
            json = response.json()

            async with aiohttp.ClientSession() as session:
                async with session.get(json[0]["url"]) as resp:
                    if resp.status != 200:
                        print(f"resp not 200 {resp}")
                        pass
                    else:
                        filename = f"./temp/cat-{ctx.author.id}"
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
            pass

        # await ctx.send(
        #     f"{choice(('Hello', 'Hi', 'Hey', 'Hiya'))} {ctx.author.mention}!"
        # )

    @Cog.listener()
    async def on_ready(self):
        if not self.bot.ready:
            self.bot.cogs_ready.ready_up("command_cat")


def setup(bot):
    bot.add_cog(Cat(bot))
