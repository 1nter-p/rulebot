import disnake
from disnake.ext import commands

from ..rulebot import Rulebot
from ..embeds import create_rules_embed
from ..rule_displays import (
    get_rule_display_channel,
    set_rule_display_channel,
    remove_rule_display_channel,
)


class RuleDisplays(commands.Cog):
    """Cog to provide rule displays"""

    def __init__(self, bot: Rulebot) -> None:
        self.bot = bot

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

    @commands.slash_command(name="update-rule-display")
    async def update_rule_display(
        self, inter: disnake.ApplicationCommandInteraction
    ) -> None:
        """Update the rule display channel for a guild."""

        try:
            channel = await get_rule_display_channel(self.bot, inter.guild_id)
        except TypeError as e:
            await inter.response.send_message(str(e), ephemeral=True)
            return

        await channel.send(embed=await create_rules_embed(self.bot.db, inter.guild_id))

        await inter.response.send_message(
            "✅ Rule display channel updated.", ephemeral=True
        )


def setup(bot: Rulebot) -> None:
    bot.add_cog(RuleDisplays(bot))
