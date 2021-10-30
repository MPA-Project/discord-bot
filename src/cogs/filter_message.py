import datetime
from discord.ext.commands import Cog, command
from discord import Message, File
from random import choice
from utils.universal import check_filter_words
import requests
import aiohttp
import aiofiles
import os

fbi_gif = [
    "https://c.tenor.com/goq48dvYSFYAAAAM/fbi-calling.gif",
    "https://c.tenor.com/m3y8M0zaeigAAAAd/fbi-swat.gif",
    "https://media0.giphy.com/media/jmSjPi6soIoQCFwaXJ/giphy-downsized.gif?cid=790b7611cc548bf1cc4a5764222e85156843401129884b3b",
    "https://media0.giphy.com/media/3o6wNPIj7WBQcJCReE/giphy-downsized.gif?cid=790b7611e1c498272d1bb1aa57a9e7b0e0592daa7220437b",
]


class FilterMessage(Cog):
    def __init__(self, bot) -> None:
        super().__init__()
        self.bot = bot

    @Cog.listener()
    async def on_message(self, message):
        def _check(m):
            return (
                m.author == message.author
                and len(m.mentions)
                and (datetime.utcnow() - m.created_at).seconds < 60
            )

        print(f"Incoming {message.content}")

        if not message.author.bot:
            # pass
            if len(list(filter(lambda m: _check(m), self.bot.cached_messages))) >= 3:
                await message.channel.send("Don't spam mentions!", delete_after=10)
            #     unmutes = await self.mute_members(
            #         message, [message.author], 5, reason="Mention spam"
            #     )

            #     if len(unmutes):
            #         await sleep(5)
            #         await self.unmute_members(message.guild, [message.author])

            filter_word = ["loli", "lolipop"]
            try:
                pass
                # if check_filter_words(filter_word, message.content):
                #     print(f"Detect message of {filter_word}")
                #     url_pic = choice(fbi_gif)
                #     print(f"Result random {url_pic}")
                #     async with aiohttp.ClientSession() as session:
                #         async with session.get(url_pic) as resp:
                #             if resp.status != 200:
                #                 print(f"resp not 200 {resp}")
                #                 pass
                #             else:
                #                 filename = f"./temp/filter-{message.author.id}"
                #                 file = await aiofiles.open(f"{filename}.gif", mode="wb")
                #                 await file.write(await resp.read())
                #                 await file.close()

                #                 await message.channel.send(file=File(f"{filename}.gif"))

                #                 if os.path.isfile(f"{filename}.gif"):
                #                     os.remove(f"{filename}.gif")
            except:
                print(f"Err")

    @Cog.listener()
    async def on_ready(self):
        if not self.bot.ready:
            self.bot.cogs_ready.ready_up("filter_message")


def setup(bot):
    bot.add_cog(FilterMessage(bot))
