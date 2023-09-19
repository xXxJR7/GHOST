import os, config, strings
from IT_S6 import it_s6, bot, redis, My_User, HNDLR, SORUCE_EMJ, MODULE, LOG
from pyrogram import filters, types, enums
from .__Help import MENU
from ..Langs import *

@it_s6.on_message(filters.command(start_log_command, HNDLR) & filters.me)
async def start_log(client, message):
    from ..Helper import eod
    if not redis.exists("s_log"):
        redis.set("s_log", "True")
        await eod(message, log_msg1)
    else:
        await eod(message, log_msg2)

@it_s6.on_message(filters.command(stop_log_command, HNDLR) & filters.me)
async def stop_log(client, message):
    from ..Helper import eod
    if not redis.exists("s_log"):
      await eod(message, log_msg3)
    else:
      redis.delete("s_log")
      await eod(message, log_msg4)

async def forward_func(client, message):
  user = await it_s6.get_messages(message.chat.id, message.id)
  chat = str(user.chat.id)
  ids = chat.replace("-100","")
  message_id = user.id
  reply_user = types.InlineKeyboardMarkup([[
                types.InlineKeyboardButton(f"{user.chat.title}",url=f"https://t.me/c/={ids}/={message_id}")
                ],
                [
                types.InlineKeyboardButton(f"{user.from_user.first_name}",url=f"https://t.me/{user.from_user.username}")
                ]])
  reply_none_user = types.InlineKeyboardMarkup([[
                types.InlineKeyboardButton(f"{user.chat.title}",url=f"https://t.me/c/={ids}/={message_id}")
                ],
                [
                types.InlineKeyboardButton(f"{user.from_user.first_name}",url=f"https://t.me/c/={ids}/={message_id}")
                ]])
  try:
     g = await it_s6.get_chat_member(message.chat.id, message.from_user.id)
  except:
     pass
  if message.mentioned:
    if not g.user.is_bot:
         if message.photo:
            s1 = await message.download()
            if message.caption:
               await bot.send_photo(int(LOG), photo =s1, caption = f"{message.caption}", reply_markup=reply_user)
               os.remove(s1)
               return
            else:
               await bot.send_photo(int(LOG), photo =s1, reply_markup=reply_user)
               os.remove(s1)
               return
         if message.sticker:
            if user.from_user.username is None:
               return await bot.send_sticker(int(LOG), sticker =message.sticker.file_id, reply_markup=reply_none_user)
            await bot.send_sticker(int(LOG), sticker =message.sticker.file_id, reply_markup=reply_user)
         if message.voice:
            s2 = await message.download()
            if user.from_user.username is None:
               await bot.send_audio(int(LOG), audio = s2, reply_markup=reply_none_user)
               os.remove(s2)
               return
            else:
               await bot.send_audio(int(LOG), audio = s2, reply_markup=reply_user)
               os.remove(s2)
               return
         if message.animation:
            s3 = await message.download()
            if user.from_user.username is None:
               await bot.send_animation(int(LOG), animation = s3, reply_markup=reply_none_user)
               os.remove(s3)
               return
            else:
               await bot.send_animation(int(LOG), animation = s3, reply_markup=reply_user)
               os.remove(s3)
               return
         if message.text:
            if user.from_user.username is None:
               return await bot.send_message(int(LOG),f"{user.text}",reply_markup=reply_none_user)
            await bot.send_message(int(LOG),f"{user.text}",reply_markup=reply_user)

back_button = types.InlineKeyboardMarkup(
            [[
             types.InlineKeyboardButton(b_button,callback_data="B_L"),
             ]]
             )

@bot.on_callback_query(filters.regex('^b_logs'))
async def b_mute(client, callback_query):
    if callback_query.from_user.id != it_s6.me.id:
       return await bot.answer_callback_query(callback_query.id, text=c_me, show_alert=True)
    return await callback_query.edit_message_text(
        strings.HELP_CMD.format(module=__mod_name__, help=__help__),
        reply_markup=back_button)

@bot.on_callback_query(filters.regex('^B_L'))
async def B_1(client, callback_query):
    if callback_query.from_user.id != it_s6.me.id:
       return await bot.answer_callback_query(callback_query.id, text=c_me, show_alert=True)
    return await callback_query.edit_message_text(
        text="", 
        reply_markup=MENU, 
        parse_mode=enums.ParseMode.MARKDOWN
    )

__mod_name__ = "Logs"  
    
__help__ = f"""  

{SORUCE_EMJ} `{HNDLR}{start_log_command}`
{start_log_us}

{SORUCE_EMJ} `{HNDLR}{stop_log_command}`
{stop_log_us}

{My_User}
"""
    
string = {"module": __mod_name__, "help": __help__}   
MODULE.append(string)
