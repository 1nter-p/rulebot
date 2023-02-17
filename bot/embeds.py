import aiosqlite
from disnake import Embed

from . import rules


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

    Raises:
        TypeError: If the rule does not exist.
    """

    return Embed(
        title=f"Rule {index}",
        description=rules.get(db, guild_id, index),
    )
