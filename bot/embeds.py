"""Various helper functions to create embeds from data."""

from disnake import Embed

from . import rules


def create_rule_embed(rule: rules.Rule) -> Embed:
    """Create an embed for a rule for the get rule command.

    Args:
        rule: The rule.

    Returns:
        The embed.
    """

    return Embed(
        title=f"Rule {rule.index}",
        description=rule.text,
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
