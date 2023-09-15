import asyncio

async def eod(message, text=None, **kwargs):
    await message.edit(text, **kwargs)
    await asyncio.sleep(5)
    await message.delete()

