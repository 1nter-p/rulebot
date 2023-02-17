from disnake import Embed

from . import rules


def create_rule_embed(index: int, text: str) -> Embed:
    """Create an embed for a rule for the get rule command.

    Args:
        text: The rule's text.

    Returns:
        The embed.
    """

    return Embed(
        title=f"Rule {index}",
        description=text,
    )


def create_rules_embed(rules: list[rules.Rule]) -> Embed:
    """Create an embed for all rules for the rule display.

    Args:
        db: The database connection.
        guild_id: The guild's ID.

    Returns:
        The embed.
    """

    embed = Embed(title="Rules", description="")

    for rule in rules:
        embed.description += f"#{rule.index}: {rule.text}\n"

    return embed
