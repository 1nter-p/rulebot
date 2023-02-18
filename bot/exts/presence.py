"""Extension to modify the bot's presence."""

import disnake
from disnake.ext import commands

from ..rulebot import Rulebot


class Presence(commands.Cog):
    """Cog that sets the bot's presence."""

    def __init__(self, bot: Rulebot) -> None:
        """Initialize the cog.

        Args:
            bot: The :cls:`Rulebot` instance.
        """
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self) -> None:
        """Called when the bot (re)connects to the gateway."""

        activity = disnake.Activity(
            type=disnake.ActivityType.watching,
            name=f"over {len(self.bot.guilds)} servers",
        )

        await self.bot.change_presence(activity=activity)


def setup(bot: Rulebot) -> None:
    """Load the Presence cog."""
    bot.add_cog(Presence(bot))
