from asyncio import sleep
from datetime import datetime
from glob import glob
from dotenv import load_dotenv
import os

from tzlocal import get_localzone

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from discord import Embed, File, DMChannel, Intents, Message
from discord.errors import HTTPException, Forbidden
from discord.ext.commands import Bot as BotBase
from discord.ext.commands import Context
from discord.ext.commands import (
    CommandNotFound,
    BadArgument,
    MissingRequiredArgument,
    CommandOnCooldown,
    CommandError,
)
from discord.ext.commands import when_mentioned_or

from ..db import db

load_dotenv()

OWNER_IDS = [int(os.environ.get("DISCORD_OWNER_ID"))]
COGS = [
    path.replace("./src/cogs/", "").replace(".py", "")
    for path in glob("./src/cogs/*.py")
]
IGNORE_EXCEPTIONS = (CommandNotFound, BadArgument)

IS_DEV = os.environ.get("MODE_DEV", False)

MAIN_GUILD = 563269331366969345
LOG_CHANNEL = 563281419888099335

ROLE_STAFF = 563269526360162313


def get_prefix(bot, message):
    prefix = db.field("SELECT Prefix FROM guilds WHERE GuildID = ?", message.guild.id)
    return when_mentioned_or(prefix)(bot, message)


class Ready(object):
    def __init__(self):
        for cog in COGS:
            setattr(self, cog, False)

    def ready_up(self, cog):
        setattr(self, cog, True)
        print(f"  {cog} cog ready")

    def all_ready(self):
        return all([getattr(self, cog) for cog in COGS])


class Bot(BotBase):
    def __init__(self):
        self.ready = False
        self.cogs_ready = Ready()

        self.guild = None
        self.scheduler = AsyncIOScheduler()
        tz = get_localzone()
        self.scheduler.configure(timezone=tz)

        try:
            with open("./data/banlist.txt", "r", encoding="utf-8") as f:
                self.banlist = [int(line.strip()) for line in f.readlines()]
        except FileNotFoundError:
            self.banlist = []

        db.autosave(self.scheduler)
        super().__init__(
            command_prefix=get_prefix, owner_ids=OWNER_IDS, intents=Intents.all()
        )

    def setup(self):
        print("cog setup")
        print(f" cog list {COGS}")
        for cog in COGS:
            # valid_cog = cog.replace('./src/cogs/', '')
            print(f" trying load {cog} cog")
            self.load_extension(f"src.cogs.{cog}")
            print(f" {cog} cog loaded")

        print("setup complete")

    def update_db(self):
        db.multiexec(
            "INSERT OR IGNORE INTO guilds (GuildID) VALUES (?)",
            ((guild.id,) for guild in self.guilds),
        )

        db.multiexec(
            "INSERT OR IGNORE INTO exp (UserID) VALUES (?)",
            ((member.id,) for member in self.guild.members if not member.bot),
        )

        # to_remove = []
        # stored_members = db.column("SELECT UserID FROM exp")
        # for id_ in stored_members:
        # 	if not self.guild.get_member(id_):
        # 		to_remove.append(id_)

        # db.multiexec("DELETE FROM exp WHERE UserID = ?",
        # 			((id_,) for id_ in to_remove))

        db.commit()

    def run(self, version):
        self.VERSION = version

        print("running setup...")
        self.setup()

        self.TOKEN = os.environ.get("DISCORD_TOKEN", None)

        print("running bot...")
        super().run(self.TOKEN, reconnect=True)

    async def process_commands(self, message):
        ctx = await self.get_context(message, cls=Context)

        if ctx.command is not None and ctx.guild is not None:
            if message.author.id in self.banlist:
                await ctx.reply("You are banned from using commands.")

            elif not self.ready:
                await ctx.reply(
                    "I'm not ready to receive commands. Please wait a few seconds."
                )

            if IS_DEV and ctx.author.id not in OWNER_IDS:
                await ctx.reply(
                    "You are not allowed to run this command during development mode."
                )

            else:
                await self.invoke(ctx)

    async def rules_reminder(self):
        pass
        # await self.stdout.send("Remember to adhere to the rules!")

    async def on_connect(self):
        print(" bot connected")

    async def on_disconnect(self):
        print("bot disconnected")

    async def on_error(self, err, *args, **kwargs):
        if err == "on_command_error":
            await args[0].send("Something went wrong.")

        await self.stdout.send(f"An error occured. {err} {kwargs}")
        raise

    async def on_command_error(self, ctx, exc):
        # print(f"on_command_error:Ctx: {ctx}")
        # print(f"on_command_error:Exc: {exc}")
        if any([isinstance(exc, error) for error in IGNORE_EXCEPTIONS]):
            pass

        elif isinstance(exc, CommandError):
            await ctx.send(exc)

        elif isinstance(exc, MissingRequiredArgument):
            await ctx.send("One or more required arguments are missing.")

        elif isinstance(exc, CommandOnCooldown):
            await ctx.send(
                f"That command is on {str(exc.cooldown.type).split('.')[-1]} cooldown. Try again in {exc.retry_after:,.2f} secs."
            )

        elif hasattr(exc, "original"):
            # if isinstance(exc.original, HTTPException):
            # 	await ctx.send("Unable to send message.")

            if isinstance(exc.original, Forbidden):
                await ctx.send("I do not have permission to do that.")

            else:
                raise exc.original

        else:
            raise exc

    async def on_ready(self):
        print(" on_ready trigger")
        if not self.ready:
            print(" bot not ready")

            print(" bot setup guild")
            self.guild = self.get_guild(MAIN_GUILD)

            print(" bot setup stdout")
            self.stdout = self.get_channel(LOG_CHANNEL)
            self.scheduler.add_job(
                self.rules_reminder,
                CronTrigger(day_of_week=0, hour=12, minute=0, second=0),
            )
            self.scheduler.start()

            print(" bot setup update_db")
            self.update_db()

            # embed = Embed(title="Now online!", description="Carberretta is now online.",
            # 			  colour=0xFF0000, timestamp=datetime.utcnow())
            # fields = [("Name", "Value", True),
            # 		  ("Another field", "This field is next to the other one.", True),
            # 		  ("A non-inline field", "This field will appear on it's own row.", False)]
            # for name, value, inline in fields:
            # 	embed.add_field(name=name, value=value, inline=inline)
            # embed.set_author(name="Carberra Tutorials", icon_url=self.guild.icon_url)
            # embed.set_footer(text="This is a footer!")
            # await channel.send(embed=embed)

            # await channel.send(file=File("./data/images/profile.png"))

            print(" bot setup update_db")
            while not self.cogs_ready.all_ready():
                await sleep(0.5)

            await self.stdout.send("Now online!")
            self.ready = True
            print(" bot ready")

            meta = self.get_cog("Meta")
            await meta.set()

        else:
            print("bot reconnected")

    async def on_message(self, message: Message):
        if not message.author.bot:
            if isinstance(message.channel, DMChannel):
                if len(message.content) < 50:
                    await message.channel.send(
                        "Your message should be at least 50 characters in length."
                    )

                else:
                    # member = self.guild.get_member(message.author.id)
                    # embed = Embed(title="Modmail",
                    # 				colour=member.colour,
                    # 				timestamp=datetime.utcnow())

                    # embed.set_thumbnail(url=member.avatar_url)

                    # fields = [("Member", member.display_name, False),
                    # 					("Message", message.content, False)]

                    # for name, value, inline in fields:
                    # 	embed.add_field(name=name, value=value, inline=inline)

                    # mod = self.get_cog("Mod")
                    # await mod.log_channel.send(embed=embed)
                    await message.channel.send("Message relayed to moderators.")

            else:
                await self.process_commands(message)

    async def log(self, message: str) -> None:
        await self.stdout.send(message)


bot = Bot()
