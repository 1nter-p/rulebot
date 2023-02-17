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

    rule_text = await rules.get(db, guild_id, index)
    if rule_text is None:
        raise TypeError("Rule does not exist.")

    return Embed(
        title=f"Rule {index}",
        description=rule_text,
    )


async def create_rules_embed(db: aiosqlite.Connection, guild_id: int) -> Embed:
    """Create an embed for all rules for the rule display.

    Args:
        db: The database connection.
        guild_id: The guild's ID.

    Returns:
        The embed.
    """

    embed = Embed(title="Rules", description="")

    for index, text in enumerate(await rules.get_all(db, guild_id)):
        embed.description += f"#{index}: {text}\n"

    return embed
