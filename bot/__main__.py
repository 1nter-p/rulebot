import os
import asyncio

import dotenv

from .rulebot import Rulebot

dotenv.load_dotenv()


async def main() -> None:
    bot = Rulebot()
    await bot.connect_to_db()
    await bot.start(os.environ["TOKEN"])


if __name__ == "__main__":
    asyncio.run(main())
