import contextlib

import disnake
from disnake.ext import commands

from .. import rules
from ..rulebot import Rulebot
from ..embeds import create_rule_embed
from ..rule_displays import sync_rule_display_channel


class Rules(commands.Cog):
    """Cog to provide rule commands."""

    def __init__(self, bot: Rulebot) -> None:
        self.bot = bot

    @commands.slash_command()
    async def rule(
        self, inter: disnake.ApplicationCommandInteraction, index: int
    ) -> None:
        """Get a rule by its index."""

        try:
            embed = await create_rule_embed(self.bot.db, inter.guild_id, index)
        except TypeError:
            await inter.response.send_message(
                "❌ That rule does not exist.", ephemeral=True
            )
        else:
            await inter.response.send_message(embed=embed)

    @commands.slash_command(name="add-rule")
    async def add_rule(
        self, inter: disnake.ApplicationCommandInteraction, text: str
    ) -> None:
        """Add a rule."""

        index = await rules.add(self.bot.db, inter.guild_id, text)

        with contextlib.suppress(TypeError):
            await sync_rule_display_channel(self.bot, inter.guild_id)

        await inter.response.send_message(f"✅ Rule {index} added.", ephemeral=True)

    @commands.slash_command(name="remove-rule")
    async def remove_rule(
        self, inter: disnake.ApplicationCommandInteraction, index: int
    ) -> None:
        """Remove a rule."""

        await rules.remove(self.bot.db, inter.guild_id, index)

        with contextlib.suppress(TypeError):
            await sync_rule_display_channel(self.bot, inter.guild_id)

        await inter.response.send_message(f"✅ Rule {index} removed.", ephemeral=True)


def setup(bot: Rulebot) -> None:
    bot.add_cog(Rules(bot))
