import disnake
import aiosqlite

from .rulebot import Rulebot


async def get_rule_display_channel(bot: Rulebot, guild_id: int) -> disnake.TextChannel:
    """Get the rule display channel for a guild.

    Args:
        guild_id: The guild's ID.

    Returns:
        The rule display channel.

    Raises:
        TypeError: If the rule display channel does not exist.
    """

    async with bot.db.execute(
        "SELECT channel_id FROM rule_displays WHERE guild_id = ?",
        (guild_id,),
    ) as cursor:
        fetch_result = await cursor.fetchone()
        if fetch_result is None:
            raise TypeError("Rule display channel does not exist.")

    channel_id = fetch_result[0]

    return await bot.fetch_channel(channel_id)


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
