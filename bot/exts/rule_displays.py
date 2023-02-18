"""Extension to provide rule display management commands."""

import disnake
from disnake.ext import commands

from ..rulebot import Rulebot
from ..rule_displays import (
    get_rule_display_channel,
    set_rule_display_channel,
    remove_rule_display_channel,
    sync_rule_display,
)


class RuleDisplays(commands.Cog):
    """Cog to provide rule displays."""

    def __init__(self, bot: Rulebot) -> None:
        """Initialize the cog.

        Args:
            bot: The :cls:`Rulebot` instance.
        """
        self.bot = bot

    @commands.slash_command(name="rule-display")
    async def rule_display(self, inter: disnake.ApplicationCommandInteraction) -> None:
        """Base command for rule display commands."""
        pass

    @rule_display.sub_command(name="get")
    async def get_rule_display(
        self, inter: disnake.ApplicationCommandInteraction
    ) -> None:
        """Get the rule display channel for a guild."""

        channel = await get_rule_display_channel(self.bot, inter.guild_id)

        if channel is None:
            await inter.response.send_message(
                "❌ No rule display channel set.", ephemeral=True
            )
        else:
            await inter.response.send_message(
                f"✅ Rule display channel is {channel.mention}.", ephemeral=True
            )

    @rule_display.sub_command(name="set")
    async def set_rule_display(
        self, inter: disnake.ApplicationCommandInteraction, channel: disnake.TextChannel
    ) -> None:
        """Set the rule display channel for a guild."""

        await set_rule_display_channel(self.bot.db, inter.guild_id, channel)
        await sync_rule_display(self.bot, inter.guild_id)

        await inter.response.send_message(
            f"✅ Rule display channel set to {channel.mention}.", ephemeral=True
        )

    @rule_display.sub_command(name="remove")
    async def remove_rule_display(
        self, inter: disnake.ApplicationCommandInteraction
    ) -> None:
        """Remove the rule display channel for a guild."""

        await remove_rule_display_channel(self.bot.db, inter.guild_id)

        await inter.response.send_message(
            "✅ Rule display channel removed.", ephemeral=True
        )


def setup(bot: Rulebot) -> None:
    """Load the RuleDisplays cog."""
    bot.add_cog(RuleDisplays(bot))
