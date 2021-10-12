from discord.ext.commands import Cog, command
from discord import Message
from random import choice


class Hi(Cog):
    def __init__(self, bot) -> None:
        super().__init__()
        self.bot = bot

    @command(name="hello", aliases=["hi"])
    async def hello(self, ctx: Message):
        await ctx.send(
            f"{choice(('Hello', 'Hi', 'Hey', 'Hiya'))} {ctx.author.mention}!"
        )

    @Cog.listener()
    async def on_ready(self):
        if not self.bot.ready:
            self.bot.cogs_ready.ready_up("command_hi")


def setup(bot):
    bot.add_cog(Hi(bot))
