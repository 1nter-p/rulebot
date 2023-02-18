"""Main entry point for the bot.

You should not run this file directly. Instead, run it via `python -m bot`.
"""

import os
import asyncio

import dotenv

from .rulebot import Rulebot

bot = Rulebot()


async def main() -> None:
    """Asynchronous entry point for the bot."""

    if not os.path.exists(".env"):
        raise FileNotFoundError(
            "No .env file found. Please create one following the template in"
            ".env.template."
        )

    dotenv.load_dotenv()

    bot = Rulebot()
    await bot.start(os.environ["TOKEN"])


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        bot.loop.run_until_complete(bot.close())
