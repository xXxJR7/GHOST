from IT_S6 import it_s6, redis
from pyrogram import filters
from .Mute import listen_gr2, listen_gr1
from .Must_Join import must_join_ls
from .prevent import Forbidden_Words_ls, preventuserbot_ls
from .Log import forward_func

@it_s6.on_message(filters.group & ~filters.me & ~filters.bot)
async def on_message(client, message):
    if message.from_user:
        if redis.get("s_log") is not None and "True" in redis.get("s_log"):
          await forward_func(client, message)
        if str(message.chat.id) in redis.smembers("mute_all"):
            await listen_gr2(client, message)
        if str(message.from_user.id) in redis.smembers(f"mute_in_chat:{message.chat.id}"):
            await listen_gr1(client, message)
        elif redis.smembers(f"must_join {message.chat.id}"):
            await must_join_ls(client, message)
        if redis.smembers(f"Forbidden_Words {message.chat.id}"):
            await Forbidden_Words_ls(client, message)
        if str(message.chat.id) in redis.smembers("Prevent_Userbot"):
            await preventuserbot_ls(client, message)
