import aiosqlite


async def get(db: aiosqlite.Connection, guild_id: int, index: int) -> str:
    """Get a rule's text.

    Args:
        db: The database connection.
        guild_id: The guild's ID.
        index: The rule's index.

    Returns:
        The rule's text.

    Raises:
        TypeError: If the rule with the given index does not exist.
    """

    async with db.execute(
        "SELECT text FROM rules WHERE guild_id = ? AND idx = ?",
        (guild_id, index),
    ) as cursor:
        rule = await cursor.fetchone()

    if rule is None:
        raise TypeError(f"Rule {index} does not exist.")

    return rule[0]


async def add(db: aiosqlite.Connection, guild_id: int, text: str) -> int:
    """Add a rule.

    Args:
        db: The database connection.
        guild_id: The guild's ID.
        text: The rule's text.

    Returns:
        The rule's index.
    """

    async with db.execute(
        "SELECT MAX(idx) FROM rules WHERE guild_id = ?",
        (guild_id,),
    ) as cursor:
        index = await cursor.fetchone()[0] or 0

    index += 1

    await db.execute(
        "INSERT INTO rules (guild_id, idx, text) VALUES (?, ?, ?)",
        (guild_id, index, text),
    )
    await db.commit()

    return index


async def remove(db: aiosqlite.Connection, guild_id: int, index: int) -> None:
    """Remove a rule.

    Args:
        db: The database connection.
        guild_id: The guild's ID.
        index: The rule's index.

    Raises:
        TypeError: If the rule with the given index does not exist.
    """

    # Ensure the rule exists since the get function raises an error if it doesn't
    await get(db, guild_id, index)

    await db.execute(
        "DELETE FROM rules WHERE guild_id = ? AND idx = ?",
        (guild_id, index),
    )
    await db.commit()
