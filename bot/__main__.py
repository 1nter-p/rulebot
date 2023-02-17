import os
import asyncio

import dotenv

from .rulebot import Rulebot


async def main() -> None:
    if not os.path.exists(".env"):
        raise FileNotFoundError(
            "No .env file found. Please create one following the template in"
            ".env.template."
        )

    dotenv.load_dotenv()

    bot = Rulebot()
    await bot.connect_to_db()
    await bot.start(os.environ["TOKEN"])


if __name__ == "__main__":
    asyncio.run(main())
