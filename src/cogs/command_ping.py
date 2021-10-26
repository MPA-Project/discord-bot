from discord.ext.commands import Cog, command
from discord import Message


class Ping(Cog):
    def __init__(self, bot) -> None:
        super().__init__()
        self.bot = bot

    @command(name="ping", help="It just ping pong return")
    async def ping(self, ctx: Message):
        await ctx.channel.send(f"Pong {ctx.author.mention}!")

    @Cog.listener()
    async def on_ready(self):
        if not self.bot.ready:
            self.bot.cogs_ready.ready_up("command_ping")


def setup(bot):
    bot.add_cog(Ping(bot))
