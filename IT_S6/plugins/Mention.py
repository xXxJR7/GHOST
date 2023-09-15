from IT_S6 import it_s6, bot, My_User, HNDLR, SORUCE_EMJ, MODULE
from pyrogram import filters, enums, types
from pyrogram.errors import SlowmodeWait
from .__Help import R_MENU
from ..Langs import *
import strings, asyncio

@it_s6.on_message(filters.command(mention_command, HNDLR) & filters.me)
async def mention(client, message):
    chat = message.chat.id
    text = message.text.split(None, 1)
    if not len(text) > 1:
       await message.delete()
       rep = message.reply_to_message
       if not rep:
        mentions = ""
        count = 0
        async for member in it_s6.get_chat_members(chat):
            if member.user:
                mentions += f" \n {member.user.mention}"
                count += 1
                if count % 6 == 0:
                   try:
                       await it_s6.send_message(chat, mentions)
                       await asyncio.sleep(1)
                   except SlowmodeWait as r:
                       await asyncio.sleep(r.value)
                       await it_s6.send_message(chat, mentions)
       else:
        mentions = rep.text
        count = 0
        async for member in it_s6.get_chat_members(chat):
            if member.user:
                mentions += f" \n {member.user.mention}"
                count += 1
                if count % 4 == 0:
                   try:
                       await it_s6.send_message(chat, mentions)
                       await asyncio.sleep(1)
                   except SlowmodeWait as r:
                       await asyncio.sleep(r.value)
                       await it_s6.send_message(chat, mentions)
    else:
        mentions = text[1]
        await message.delete()
        count = 0
        async for member in it_s6.get_chat_members(chat):
            if member.user:
                mentions += f" \n {member.user.mention}"
                count += 1
                if count % 4 == 0:
                   try:
                       await it_s6.send_message(chat, mentions)
                       await asyncio.sleep(1)
                   except SlowmodeWait as r:
                       await asyncio.sleep(r.value)
                       await it_s6.send_message(chat, mentions)

back_button = types.InlineKeyboardMarkup(
            [[
             types.InlineKeyboardButton(b_button,callback_data="B_ment"),
             ]]
             )

@bot.on_callback_query(filters.regex('^b_mention'))
async def b_mention(client, callback_query):
    if callback_query.from_user.id != it_s6.me.id:
       return await bot.answer_callback_query(callback_query.id, text=c_me, show_alert=True)
    return await callback_query.edit_message_text(
        strings.HELP_CMD.format(module=__mod_name__, help=__help__),
        reply_markup=back_button)

@bot.on_callback_query(filters.regex('^B_ment'))
async def B_ment(client, callback_query):
    if callback_query.from_user.id != it_s6.me.id:
       return await bot.answer_callback_query(callback_query.id, text=c_me, show_alert=True)
    return await callback_query.edit_message_text(
        text="", 
        reply_markup=R_MENU, 
        parse_mode=enums.ParseMode.MARKDOWN
    )

__mod_name__ = "Mention"  
    
__help__ = f"""  

{SORUCE_EMJ} `{HNDLR}{mention_command}`
{mention_us}

{My_User}
"""
    
string = {"module": __mod_name__, "help": __help__}   
MODULE.append(string)