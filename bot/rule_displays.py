"""Abstraction for interacting with rule displays."""

import disnake
import aiosqlite

from bot.embeds import create_rules_embed

from . import rules
from .rulebot import Rulebot


async def get_rule_display_channel(bot: Rulebot, guild_id: int) -> disnake.TextChannel:
    """Get the rule display channel for a guild.

    Args:
        guild_id: The guild's ID.

    Returns:
        The rule display channel.
    """

    async with bot.db.execute(
        "SELECT channel_id FROM rule_displays WHERE guild_id = ?",
        (guild_id,),
    ) as cursor:
        fetch_result = await cursor.fetchone()

    if fetch_result is None:
        return None

    channel_id = fetch_result[0]

    try:
        return await bot.fetch_channel(channel_id)
    except disnake.NotFound:
        await remove_rule_display_channel(bot.db, guild_id)
        return None


async def set_rule_display_channel(
    db: aiosqlite.Connection, guild_id: int, channel: disnake.TextChannel
) -> None:
    """Set the rule display channel for a guild.

    Args:
        db: The database connection.
        guild_id: The guild's ID.
        channel: The rule display channel.
    """

    await db.execute(
        "INSERT INTO rule_displays (guild_id, channel_id) VALUES (?, ?)",
        (guild_id, channel.id),
    )
    await db.commit()


async def remove_rule_display_channel(db: aiosqlite.Connection, guild_id: int) -> None:
    """Remove the rule display channel for a guild.

    Args:
        db: The database connection.
        guild_id: The guild's ID.
    """

    await db.execute("DELETE FROM rule_displays WHERE guild_id = ?", (guild_id,))
    await db.commit()


async def sync_rule_display(bot: Rulebot, guild_id: int) -> None:
    """Sync the rule display for a guild.

    Args:
        bot: The bot.
        guild_id: The guild's ID.

    Raises:
        TypeError: If the rule display channel does not exist.
    """

    channel = await get_rule_display_channel(bot, guild_id)
    if channel is None:
        raise TypeError("Rule display channel does not exist.")

    await channel.purge()

    embed = create_rules_embed(await rules.get_all(bot.db, guild_id))
    await channel.send(embed=embed)
