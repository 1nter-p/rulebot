import os
import aiosqlite
import disnake
from disnake.ext import commands


class Rulebot(commands.InteractionBot):
    """:cls:`disnake.ext.commands.InteractionBot` subclass that provides all Rulebot
    functionality.

    After instantiating, make sure to call :meth:`connect_to_db` before starting
    otherwise the bot will not work.

    Attributes:
        db: The database connection.
    """

    def __init__(self) -> None:
        super().__init__(intents=disnake.Intents.default())

        self.db: aiosqlite.Connection

        self._load_all_extensions()

    async def on_ready(self) -> None:
        print("Ready!")

    def _load_all_extensions(self) -> None:
        """Load all extensions in the exts directory."""

        for ext in os.listdir("bot/exts"):
            if ext.endswith(".py"):
                self.load_extension(f"bot.exts.{ext.removesuffix('.py')}")

    async def connect_to_db(self) -> None:
        """Connect to the database. Ideally, this should only be called once."""

        self.db = await aiosqlite.connect(os.environ["DB_PATH"])
        await self._run_init_sql()

    async def _run_init_sql(self) -> None:
        """Run the init.sql file through the database."""

        with open("init.sql") as file:
            await self.db.executescript(file.read())
