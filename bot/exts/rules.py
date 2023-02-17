import contextlib

import disnake
from disnake.ext import commands

from .. import rules
from ..rulebot import Rulebot
from ..embeds import create_rule_embed
from ..rule_displays import sync_rule_display


class Rules(commands.Cog):
    """Cog to provide rule commands."""

    def __init__(self, bot: Rulebot) -> None:
        self.bot = bot

    @commands.slash_command()
    async def rule(self, inter: disnake.ApplicationCommandInteraction) -> None:
        """Base command for rule commands."""
        pass

    @rule.sub_command(name="get")
    async def get_rule(
        self, inter: disnake.ApplicationCommandInteraction, index: int
    ) -> None:
        """Get a rule by its index."""

        rule = await rules.get(self.bot.db, inter.guild_id, index)
        if rule is None:
            await inter.response.send_message(
                f"❌ Rule {index} not found.", ephemeral=True
            )
            return

        await self.silently_sync_rule_display(inter.guild_id)

        await inter.response.send_message(embed=create_rule_embed(rule), ephemeral=True)

    @rule.sub_command(name="add")
    async def add_rule(
        self, inter: disnake.ApplicationCommandInteraction, text: str
    ) -> None:
        """Add a rule."""

        rule = await rules.add(self.bot.db, inter.guild_id, text)

        await self.silently_sync_rule_display(inter.guild_id)

        await inter.response.send_message(
            f"✅ Rule {rule.index} added.",
            embed=create_rule_embed(rule.index, rule.text),
            ephemeral=True,
        )

    @rule.sub_command(name="remove")
    async def remove_rule(
        self, inter: disnake.ApplicationCommandInteraction, index: int
    ) -> None:
        """Remove a rule."""

        await rules.remove(self.bot.db, inter.guild_id, index)

        await self.silently_sync_rule_display(inter.guild_id)

        await inter.response.send_message(f"✅ Rule {index} removed.", ephemeral=True)

    async def silently_sync_rule_display(self, guild_id: int) -> None:
        """Silently sync the rule display channel for a guild."""

        with contextlib.suppress(TypeError):
            await sync_rule_display(self.bot, guild_id)


def setup(bot: Rulebot) -> None:
    """Load the Rules cog."""
    bot.add_cog(Rules(bot))
