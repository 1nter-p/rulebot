from dataclasses import dataclass

import aiosqlite


@dataclass
class Rule:
    """Represents a rule."""

    index: int
    text: str


async def get(db: aiosqlite.Connection, guild_id: int, index: int) -> Rule | None:
    """Get a rule's text.

    Args:
        db: The database connection.
        guild_id: The guild's ID.
        index: The rule's index.

    Returns:
        The rule.
    """

    async with db.execute(
        "SELECT idx, text FROM rules WHERE guild_id = ? AND idx = ?",
        (guild_id, index),
    ) as cursor:
        rule = await cursor.fetchone()

    if rule is None:
        return None

    return Rule(rule[0], rule[1])


async def get_all(db: aiosqlite.Connection, guild_id: int) -> list[Rule]:
    """Get all rules for a guild.

    Args:
        db: The database connection.
        guild_id: The guild's ID.

    Returns:
        The rules.
    """

    async with db.execute(
        "SELECT idx, text FROM rules WHERE guild_id = ? ORDER BY idx",
        (guild_id,),
    ) as cursor:
        return [Rule(rule[0], rule[1]) async for rule in cursor]


async def get_next_index(db: aiosqlite.Connection, guild_id: int) -> int:
    """Get the next rule index for a guild.

    Args:
        db: The database connection.
        guild_id: The guild's ID.

    Returns:
        The next rule index.
    """

    async with db.execute(
        "SELECT MAX(idx) FROM rules WHERE guild_id = ?",
        (guild_id,),
    ) as cursor:
        index = (await cursor.fetchone())[0] or 0

    return index + 1


async def add(db: aiosqlite.Connection, guild_id: int, text: str) -> Rule:
    """Add a rule.

    Args:
        db: The database connection.
        guild_id: The guild's ID.
        text: The rule's text.

    Returns:
        The new rule.
    """

    index = await get_next_index(db, guild_id)

    await db.execute(
        "INSERT INTO rules (guild_id, idx, text) VALUES (?, ?, ?)",
        (guild_id, index, text),
    )
    await db.commit()

    return Rule(index, text)


async def remove(db: aiosqlite.Connection, guild_id: int, index: int) -> None:
    """Remove a rule.

    Args:
        db: The database connection.
        guild_id: The guild's ID.
        index: The rule's index.

    Raises:
        TypeError: If the rule does not exist.
    """

    if await get(db, guild_id, index) is None:
        raise TypeError("Rule does not exist.")

    await db.execute(
        "DELETE FROM rules WHERE guild_id = ? AND idx = ?",
        (guild_id, index),
    )

    # Change the other rules after the removed rule to have the correct index
    async with db.execute(
        "SELECT idx FROM rules WHERE guild_id = ? AND idx > ?",
        (guild_id, index),
    ) as cursor:
        async for row in cursor:
            await db.execute(
                "UPDATE rules SET idx = ? WHERE guild_id = ? AND idx = ?",
                (row[0] - 1, guild_id, row[0]),
            )

    await db.commit()
