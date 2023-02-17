import disnake
from disnake.ext import commands

from ..rulebot import Rulebot
from ..rule_displays import (
    set_rule_display_channel,
    remove_rule_display_channel,
)


class RuleDisplays(commands.Cog):
    """Cog to provide rule displays"""

    def __init__(self, bot: Rulebot) -> None:
        self.bot = bot

    @commands.slash_command(name="get-rule-display")
    async def get_rule_display(
        self, inter: disnake.ApplicationCommandInteraction
    ) -> None:
        """Get the rule display channel for a guild."""

        channel = await self.bot.get_rule_display_channel(inter.guild_id)

        if channel is None:
            await inter.response.send_message(
                "❌ No rule display channel set.", ephemeral=True
            )
        else:
            await inter.response.send_message(
                f"✅ Rule display channel is {channel.mention}.", ephemeral=True
            )

    @commands.slash_command(name="set-rule-display")
    async def set_rule_display(
        self, inter: disnake.ApplicationCommandInteraction, channel: disnake.TextChannel
    ) -> None:
        """Set the rule display channel for a guild."""

        await set_rule_display_channel(self.bot.db, inter.guild_id, channel)

        await inter.response.send_message(
            f"✅ Rule display channel set to {channel.mention}.", ephemeral=True
        )

    @commands.slash_command(name="remove-rule-display")
    async def remove_rule_display(
        self, inter: disnake.ApplicationCommandInteraction
    ) -> None:
        """Remove the rule display channel for a guild."""

        await remove_rule_display_channel(self.bot.db, inter.guild_id)

        await inter.response.send_message(
            "✅ Rule display channel removed.", ephemeral=True
        )


def setup(bot: Rulebot) -> None:
    bot.add_cog(RuleDisplays(bot))
