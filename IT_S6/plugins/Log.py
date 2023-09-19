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
