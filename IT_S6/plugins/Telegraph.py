from IT_S6 import it_s6, bot, My_User, SORUCE_EMJ, HNDLR, MODULE
from ..Helper import eod
from datetime import datetime
from pyrogram import filters, enums, types
from .__Help import R_MENU
from ..Langs import *
from telegraph import Telegraph, upload_file
import os, strings

telegraph = Telegraph()
r = telegraph.create_account(short_name="Sa3ed")
auth_url = r["auth_url"]

@it_s6.on_message(filters.command(telegraph_command, HNDLR) & filters.me)
async def telegraph(client, message):
        if not message.reply_to_message:
           return await eod(message, c_media)
        if not message.reply_to_message.media:
           return await eod(message, c_media)
        await message.edit(telegraph_msg1)
        start = datetime.now()
        if message.reply_to_message.video:
           photo_path = "./sa3ed.mp4"
        if message.reply_to_message.photo:
           photo_path = "./sa3ed.jpg"
        await message.reply_to_message.download(photo_path)
        await message.edit(telegraph_msg2)
        end = datetime.now()
        ms = (end - start).seconds
        await message.edit(telegraph_msg3.format(SORUCE_EMJ, SORUCE_EMJ, upload_file(photo_path)[0], SORUCE_EMJ, ms), disable_web_page_preview=True)
        os.remove(photo_path)

back_button = types.InlineKeyboardMarkup(
            [[
             types.InlineKeyboardButton(b_button,callback_data="B_teleg"),
             ]]
             )

@bot.on_callback_query(filters.regex('^b_telegraph'))
async def b_telegraph(client, callback_query):
    if callback_query.from_user.id != it_s6.me.id:
       return await bot.answer_callback_query(callback_query.id, text=c_me, show_alert=True)
    return await callback_query.edit_message_text(
        strings.HELP_CMD.format(module=__mod_name__, help=__help__),
        reply_markup=back_button)

@bot.on_callback_query(filters.regex('^B_teleg'))
async def B_teleg(client, callback_query):
    if callback_query.from_user.id != it_s6.me.id:
       return await bot.answer_callback_query(callback_query.id, text=c_me, show_alert=True)
    return await callback_query.edit_message_text(
        text="", 
        reply_markup=R_MENU, 
        parse_mode=enums.ParseMode.MARKDOWN
    )

__mod_name__ = "Telegraph"  
    
__help__ = f"""  

{SORUCE_EMJ} `{HNDLR}{telegraph_command}`
{telegraph_us}

{My_User}
"""
    
    
string = {"module": __mod_name__, "help": __help__}   
MODULE.append(string)
