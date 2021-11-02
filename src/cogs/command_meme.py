from discord.ext.commands import Cog, command
from discord import Message
import aiohttp
import aiofiles
import os
from discord import File


class Meme(Cog):
    def __init__(self, bot) -> None:
        super().__init__()
        self.bot = bot

    @command(name="rickroll", hidden=True)
    async def rickroll(self, ctx: Message):
        url_pic = "https://c.tenor.com/x8v1oNUOmg4AAAAd/rickroll-roll.gif"
        async with aiohttp.ClientSession() as session:
            async with session.get(url_pic) as resp:
                if resp.status != 200:
                    print(f"resp not 200 {resp}")
                    pass
                else:
                    filename = f"./temp/rickroll-{ctx.author.id}"
                    file = await aiofiles.open(f"{filename}.gif", mode="wb")
                    await file.write(await resp.read())
                    await file.close()

                    await ctx.send(file=File(f"{filename}.gif"))

                    if os.path.isfile(f"{filename}.gif"):
                        os.remove(f"{filename}.gif")

    @Cog.listener()
    async def on_ready(self):
        if not self.bot.ready:
            self.bot.cogs_ready.ready_up("command_meme")


def setup(bot):
    bot.add_cog(Meme(bot))
