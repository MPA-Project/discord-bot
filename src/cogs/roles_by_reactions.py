from datetime import datetime, timedelta
from random import choice

from discord import Embed
from discord.utils import get
from discord.ext.commands import Cog
from discord.ext.commands import command, has_permissions

from ..db import db

roles_by_reaction_channel = 896038913200762900
roles_by_reaction_message = 896651569121071105


class RolesByReactions(Cog):
    def __init__(self, bot):
        self.bot = bot
        self.polls = []
        self.giveaways = []

    @Cog.listener()
    async def on_ready(self):
        if not self.bot.ready:
            self.roles = {
                "🦄": self.bot.guild.get_role(896015620452253786),  # Pony
                "👹": self.bot.guild.get_role(896016607564955658),  # Anime
            }
            self.role_remove = "💔"
            self.reaction_message = await self.bot.get_channel(
                roles_by_reaction_channel
            ).fetch_message(roles_by_reaction_message)
            self.bot.cogs_ready.ready_up("roles_by_reactions")

    @Cog.listener()
    async def on_raw_reaction_add(self, payload):
        if self.bot.ready and payload.message_id == self.reaction_message.id:
            if payload.emoji.name == self.role_remove:
                for role in self.roles.values():
                    await payload.member.remove_roles(
                        role, reason="Colour role reaction [removed]."
                    )
            else:
                await payload.member.add_roles(
                    self.roles[payload.emoji.name],
                    reason="Colour role reaction [added].",
                )
                if payload.emoji.name in self.roles:
                    pass

            await self.reaction_message.remove_reaction(payload.emoji, payload.member)


def setup(bot):
    bot.add_cog(RolesByReactions(bot))
