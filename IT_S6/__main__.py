from pyrogram import enums, idle
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, BotCommand
from IT_S6 import it_s6, bot, redis, version, SORUCE_EMJ, LOG
from IT_S6.plugins import ALL_PLUGINS
from IT_S6.plugins.Autoname import auto_italia
from .Langs import *
import asyncio, importlib, config

DEV_profile = InlineKeyboardMarkup(
            [[
             InlineKeyboardButton("𝗠𝗔𝗛𝗠𝗢𝗨𝗗",url=f"https://t.me/xXx_JR"),
             ]]
             )

async def sa3ed_startup():
    for module in ALL_PLUGINS:
        importlib.import_module("IT_S6.plugins." + module)
    s1 = await it_s6.get_me()
    own_men = s1.first_name
    if str(s1.id) not in redis.smembers("SUDOS"):
       redis.sadd("SUDOS", s1.id)
    await bot.start()
    await bot.set_bot_commands([BotCommand("start", "Start")])
    if redis.exists("Restart"):
       res_id = int(redis.get(("Restart")))
       try:
          last_restart_msg_ids = int(redis.get('last_restart_msg_ids'))
          async for Sa3ed in it_s6.get_dialogs():
             if Sa3ed.chat.type is enums.ChatType.PRIVATE:
                if res_id == Sa3ed.chat.id:
                   await it_s6.edit_message_text(res_id, last_restart_msg_ids, res_msg4)
             else:
                await it_s6.edit_message_text(res_id, last_restart_msg_ids, res_msg4)
       except Exception:
          pass
       redis.delete("Restart")
    if not config.START_IMG:
       await bot.send_message(int(LOG), text=s_msg.format(SORUCE_EMJ, SORUCE_EMJ, own_men, SORUCE_EMJ, config.BOT_USER, SORUCE_EMJ, version, SORUCE_EMJ, len(ALL_PLUGINS) - 3), reply_markup=DEV_profile)
    elif config.START_IMG.endswith(".mp4"):
       await bot.send_video(int(LOG), video=config.START_IMG, caption=s_msg.format(SORUCE_EMJ, SORUCE_EMJ, own_men, SORUCE_EMJ, config.BOT_USER, SORUCE_EMJ, version, SORUCE_EMJ, len(ALL_PLUGINS) - 3), reply_markup=DEV_profile)
    elif config.START_IMG.endswith(".jpg"):
       await bot.send_photo(int(LOG), photo=config.START_IMG, caption=s_msg.format(SORUCE_EMJ, SORUCE_EMJ, own_men, SORUCE_EMJ, config.BOT_USER, SORUCE_EMJ, version, SORUCE_EMJ, len(ALL_PLUGINS) - 3), reply_markup=DEV_profile)
    await auto_italia()
    await idle()

if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(sa3ed_startup())
