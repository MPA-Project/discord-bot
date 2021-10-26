from discord.ext.commands import (
    Cog,
    Greedy,
    command,
    has_permissions,
    bot_has_permissions,
    has_role,
)
from datetime import datetime, timedelta
from typing import Optional
from discord import Message, Member
from src.bot import ROLE_STAFF


class AdminClearMessage(Cog):
    def __init__(self, bot) -> None:
        super().__init__()
        self.bot = bot

    @command(name="clear", aliases=["cls", "purge"], hidden=True)
    @bot_has_permissions(manage_messages=True)
    @has_permissions(manage_messages=True)
    @has_role(ROLE_STAFF)
    async def clear_messages(
        self, ctx: Message, targets: Greedy[Member], limit: Optional[int] = 1
    ):
        def _check(message):
            return not len(targets) or message.author in targets

        if 0 < limit <= 100:
            with ctx.channel.typing():
                await ctx.message.delete()
                deleted = await ctx.channel.purge(
                    limit=limit,
                    after=datetime.utcnow() - timedelta(days=14),
                    check=_check,
                )

                await ctx.send(f"Deleted {len(deleted):,} messages.", delete_after=5)

        else:
            await ctx.send("The limit provided is not within acceptable bounds.")

    @Cog.listener()
    async def on_ready(self):
        if not self.bot.ready:
            self.bot.cogs_ready.ready_up("command_admin_clear_message")


def setup(bot):
    bot.add_cog(AdminClearMessage(bot))
