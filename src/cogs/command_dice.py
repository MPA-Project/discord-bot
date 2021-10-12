from discord.ext.commands import Cog, command, cooldown, BucketType
from discord import Message
from random import randint


class Dice(Cog):
    def __init__(self, bot) -> None:
        super().__init__()
        self.bot = bot

    @command(name="dice", aliases=["roll"])
    @cooldown(1, 60, BucketType.user)
    async def dice(self, ctx: Message, die_string: str):
        try:
            dice, value = (int(term) for term in die_string.split("d"))

            if dice <= 25:
                rolls = [randint(1, value) for _ in range(dice)]

                await ctx.send(" + ".join([str(r) for r in rolls]) + f" = {sum(rolls)}")

            else:
                await ctx.send(
                    "I can't roll that many dice. Please try a lower number."
                )
        except:
            await ctx.send("Input value must valid, example: !dice 2d5")

    @Cog.listener()
    async def on_ready(self):
        if not self.bot.ready:
            self.bot.cogs_ready.ready_up("command_dice")


def setup(bot):
    bot.add_cog(Dice(bot))
