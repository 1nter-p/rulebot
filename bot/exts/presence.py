import disnake
from disnake.ext import commands

from ..rulebot import Rulebot


class Presence(commands.Cog):
    """Cog that sets the presence."""

    def __init__(self, bot: Rulebot) -> None:
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self) -> None:
        activity = disnake.Activity(
            type=disnake.ActivityType.watching,
            name=f"over {len(self.bot.guilds)} servers",
        )

        await self.bot.change_presence(activity=activity)


def setup(bot: Rulebot) -> None:
    """Load the Presence cog."""
    bot.add_cog(Presence(bot))
