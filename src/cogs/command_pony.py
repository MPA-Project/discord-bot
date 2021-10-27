from discord.ext.commands import Cog, command, CommandError
from discord import Message, File
import aiohttp
import aiofiles
import os
import urllib
from PIL import Image
import requests
from derpibooru import Search, sort
from bs4 import BeautifulSoup


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

                            await ctx.reply(f"Source: <{img.url}>")
                            await ctx.send(file=File(f"{filename}.jpg"))

                            if os.path.isfile(f"{filename}.jpg"):
                                os.remove(f"{filename}.jpg")
                            if os.path.isfile(f"{filename}_temp"):
                                os.remove(f"{filename}_temp")
            except Exception as ex:
                print(f"err {ex}")
                raise CommandError(f"Something went wrong, try again leter")

    @command(name="ponywall", help="Show random pony wallpaper images")
    async def ponywall(self, ctx: Message):
        url = "https://www.mylittlewallpaper.com/c/my-little-pony/api/v1/random.json?limit=1"

        try:
            response = requests.get(url)
            base_json = response.json()
        except Exception as ex:
            print(f"Error {ex}")
            raise CommandError(f"Something went wrong, try again leter")

        try:
            resp = urllib.request.urlopen(base_json["result"][0]["downloadurl"])
            content = resp.read().decode("utf8")
        except ValueError as error:
            print(f"Error {error}")
            raise CommandError(f"Something went wrong, try again leter")

        try:
            soup = BeautifulSoup(content, "html.parser")
            download_button = soup.find("a", {"class": "download button"})
            download_link = download_button["href"]
        except Exception as error:
            print(f"Error {error}")
            raise CommandError(f"Something went wrong, try again leter")

        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(download_link) as resp:
                    if resp.status != 200:
                        print(f"resp not 200 {resp}")
                        pass
                    else:
                        filename = f"./temp/pony-wall-{ctx.author.id}"
                        file = await aiofiles.open(f"{filename}_temp", mode="wb")
                        await file.write(await resp.read())
                        await file.close()

                        im = Image.open(f"{filename}_temp")
                        rgb_im = im.convert("RGB")
                        rgb_im.save(f"{filename}.jpg")

                        await ctx.reply(
                            "Source: <{}>".format(base_json["result"][0]["downloadurl"])
                        )
                        await ctx.send(file=File(f"{filename}.jpg"))

                        if os.path.isfile(f"{filename}.jpg"):
                            os.remove(f"{filename}.jpg")
                        if os.path.isfile(f"{filename}_temp"):
                            os.remove(f"{filename}_temp")
        except Exception as ex:
            print(f"Error {ex}")
            raise CommandError(f"Something went wrong, try again leter")

    @Cog.listener()
    async def on_ready(self):
        if not self.bot.ready:
            self.bot.cogs_ready.ready_up("command_pony")


def setup(bot):
    bot.add_cog(Pony(bot))
