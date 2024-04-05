import common
import asyncio
from pyrogram import Client, enums


async def main():
    async with Client(
        common.SESSION_FILE,
        common.CFG.api_id,
        common.CFG.api_hash,
        proxy=common.CFG.proxy_pyrogram_json,
        parse_mode=enums.ParseMode.DISABLED,
    ) as app:
        await app.join_chat("DoO_o")


if __name__ == "__main__":
    asyncio.run(main())
