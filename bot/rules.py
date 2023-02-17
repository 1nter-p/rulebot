import aiosqlite


async def get(db: aiosqlite.Connection, guild_id: int, index: int) -> str:
    """Get a rule's text.

    Args:
        db: The database connection.
        guild_id: The guild's ID.
        index: The rule's index.

    Returns:
        The rule's text.
    """

    async with db.execute(
        "SELECT text FROM rules WHERE guild_id = ? AND idx = ?",
        (guild_id, index),
    ) as cursor:
        rule = await cursor.fetchone()

    if rule is None:
        return None

    return rule[0]


async def get_all(db: aiosqlite.Connection, guild_id: int) -> list[str]:
    """Get all rules.

    Args:
        db: The database connection.
        guild_id: The guild's ID.

    Returns:
        The rules.
    """

    async with db.execute(
        "SELECT text FROM rules WHERE guild_id = ? ORDER BY idx",
        (guild_id,),
    ) as cursor:
        return [rule[0] async for rule in cursor]


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
        index = (await cursor.fetchone())[0] or 0

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
