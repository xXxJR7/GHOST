import asyncio
from IT_S6 import it_s6

async def sod(message, text=None, **kwargs):
    m = await it_s6.send_message(message, text, **kwargs)
    await asyncio.sleep(5)
    await it_s6.delete_messages(message, m.id)