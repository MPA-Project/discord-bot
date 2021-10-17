from discord import Forbidden, Embed, Member, File
from discord.ext.commands import Cog
from discord.ext.commands import command
from utils.welcome_image import image_generator
import io
import aiohttp
import pyvips
import aiofiles

from ..db import db

welcome_channel = 896019708724264970


class Welcome(Cog):
    def __init__(self, bot):
        self.bot = bot

    @Cog.listener()
    async def on_ready(self):
        if not self.bot.ready:
            self.bot.cogs_ready.ready_up("welcome")

    @Cog.listener()
    async def on_member_join(self, member: Member):
        db.execute("INSERT INTO exp (UserID) VALUES (?)", member.id)

        # embed = Embed(
        #     title=f"Welcome to **{member.guild.name}** {member.mention}!",
        # )
        # embed.set_image(url=member.avatar_url)
        # await self.bot.get_channel(welcome_channel).send(
        #     f"Welcome to **{member.guild.name}** {member.mention}!"
        # )

        async with aiohttp.ClientSession() as session:
            welcome_url = image_generator(
                name=member.display_name, avatar=member.avatar_url
            )
            print(f"Welcome {welcome_url}")
            async with session.get(welcome_url) as resp:
                if resp.status != 200:
                    await self.bot.get_channel(welcome_channel).send(
                        f"Welcome to **{member.guild.name}** {member.mention}!"
                    )
                else:
                    await self.bot.get_channel(welcome_channel).send(
                        f"Welcome to **{member.guild.name}** {member.mention}!"
                    )

                    filename = f"./temp/welcome-{member.id}"
                    file = await aiofiles.open(f"{filename}.svg", mode="wb")
                    await file.write(await resp.read())
                    await file.close()
                    temp_image = pyvips.Image.new_from_file(f"{filename}.svg", dpi=300)
                    temp_image.write_to_file(f"{filename}.png")
                    # await self.bot.get_channel(welcome_channel).send(
                    #     file=File(f"{filename}.png")
                    # )

        try:
            await member.send(f"Welcome to **{member.guild.name}**! Enjoy your stay!")

        except Forbidden:
            pass

    @Cog.listener()
    async def on_member_remove(self, member: Member):
        db.execute("DELETE FROM exp WHERE UserID = ?", member.id)
        await self.bot.get_channel(welcome_channel).send(
            f"{member.display_name} has left."
        )


def setup(bot):
    bot.add_cog(Welcome(bot))
