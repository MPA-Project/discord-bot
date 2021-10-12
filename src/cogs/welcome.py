from discord import Forbidden, Embed, Member
from discord.ext.commands import Cog
from discord.ext.commands import command

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
        await self.bot.get_channel(welcome_channel).send(
            f"Welcome to **{member.guild.name}** {member.mention}!"
        )

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
