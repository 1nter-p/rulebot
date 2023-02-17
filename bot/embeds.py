import aiosqlite
from disnake import Embed


async def create_rule_embed(
    db: aiosqlite.Connection, guild_id: int, index: int
) -> Embed:
    """Create an embed for a rule for the get rule command.

    Args:
        db: The database connection.
        guild_id: The guild's ID.
        index: The rule's index.

    Returns:
        The embed.
    """

    async with db.execute(
        "SELECT text FROM rules WHERE guild_id = ? AND idx = ?",
        (guild_id, index),
    ) as cursor:
        rule = await cursor.fetchone()

    if rule is None:
        raise TypeError(f"Rule {index} does not exist.")

    rule_text = rule[0]

    return Embed(
        title=f"Rule {index}",
        description=rule_text,
        color=0x00FF00,
    )
