"""Contains the Rulebot class, which is the main bot class."""

import os
import aiosqlite
import disnake
from disnake.ext import commands


class Rulebot(commands.InteractionBot):
    """:cls:`disnake.ext.commands.InteractionBot` subclass with Rulebot functionality.

    Attributes:
        db: The database connection.
    """

    def __init__(self) -> None:
        """Initialize the bot."""

        super().__init__(intents=disnake.Intents.default())

        self.db: aiosqlite.Connection

        self.load_all_extensions()

    async def on_ready(self) -> None:
        """Called when the bot (re)connects to the gateway."""
        print("Ready!")

    async def start(self, token: str) -> None:
        """Start the bot.

        This is overriden by Rulebot to connect to the database in an async context.

        Args:
            token: The bot token.
        """

        await self.connect_to_db()

        await super().start(token, reconnect=True)

    def load_all_extensions(self) -> None:
        """Load all extensions in the exts directory."""

        for ext in os.listdir("bot/exts"):
            if ext.endswith(".py"):
                self.load_extension(f"bot.exts.{ext.removesuffix('.py')}")

    async def connect_to_db(self) -> None:
        """Connect to the database. Ideally, this should only be called once."""

        self.db = await aiosqlite.connect(os.environ["DB_PATH"])
        await self.run_init_sql()

    async def run_init_sql(self) -> None:
        """Run the init.sql file through the database."""

        with open("init.sql") as file:
            await self.db.executescript(file.read())
