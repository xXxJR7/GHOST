from IT_S6 import it_s6, bot, redis, My_User, SORUCE_EMJ, HNDLR, MODULE
from pyrogram import filters, enums, types
from .__Help import R_MENU
from ..Langs import *
import asyncio, sys, subprocess, strings

@it_s6.on_message(filters.command(restart_command, HNDLR) & filters.me)
async def restart_script(client, message):
    redis.set("Restart", int(message.chat.id))
    await message.edit(res_msg1)
    await asyncio.sleep(0.5) 
    await message.edit(res_msg2)
    await asyncio.sleep(0.5)
    r = await message.edit(res_msg3)
    await asyncio.sleep(0.5)
    redis.set('last_restart_msg_ids', int(r.id))
    subprocess.Popen([sys.executable, "-B", "-m", "IT_S6"], close_fds=True)
    sys.exit(0)

back_button = types.InlineKeyboardMarkup(
            [[
             types.InlineKeyboardButton(b_button,callback_data="B_res"),
             ]]
             )

@bot.on_callback_query(filters.regex('^b_restart'))
async def b_restart(client, callback_query):
    if callback_query.from_user.id != it_s6.me.id:
       return await bot.answer_callback_query(callback_query.id, text=c_me, show_alert=True)
    return await callback_query.edit_message_text(
        strings.HELP_CMD.format(module=__mod_name__, help=__help__),
        reply_markup=back_button)

@bot.on_callback_query(filters.regex('^B_res'))
async def B_res(client, callback_query):
    if callback_query.from_user.id != it_s6.me.id:
       return await bot.answer_callback_query(callback_query.id, text=c_me, show_alert=True)
    return await callback_query.edit_message_text(
        text="", 
        reply_markup=R_MENU, 
        parse_mode=enums.ParseMode.MARKDOWN
    )

__mod_name__ = "Restart"  
    
__help__ = f"""  

{SORUCE_EMJ} `{HNDLR}{restart_command}`
{restart_us}

{My_User}
"""
    
    
string = {"module": __mod_name__, "help": __help__}   
MODULE.append(string)