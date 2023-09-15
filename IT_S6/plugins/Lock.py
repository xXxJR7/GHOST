from IT_S6 import it_s6, bot, My_User, HNDLR, SORUCE_EMJ, MODULE
from pyrogram import filters, enums, types
from pyrogram.types import ChatPermissions
from ..Langs import *
from .__Help import MENU
import strings

@it_s6.on_message(filters.command(lock_command, HNDLR) & filters.me)
async def lock_chat(client, message):
    from ..Helper import eod
    me = await it_s6.get_chat_member(message.chat.id, it_s6.me.id)
    if me.status not in [enums.ChatMemberStatus.OWNER, enums.ChatMemberStatus.ADMINISTRATOR]:
         return await eod(message, c_admin)
    chat = await it_s6.get_chat(message.chat.id)
    if chat.permissions.can_send_messages is True:
       await it_s6.set_chat_permissions(message.chat.id, ChatPermissions(can_send_messages=False))
       return await eod(message, lock_msg1)
    await eod(message, lock_msg2)

@it_s6.on_message(filters.command(unlock_command, HNDLR) & filters.me)
async def open_chat(client, message):
    from ..Helper import eod
    me = await it_s6.get_chat_member(message.chat.id, it_s6.me.id)
    if me.status not in [enums.ChatMemberStatus.OWNER, enums.ChatMemberStatus.ADMINISTRATOR]:
         return await eod(message, c_admin)
    chat = await it_s6.get_chat(message.chat.id)
    if chat.permissions.can_send_messages is False:
       await it_s6.set_chat_permissions(message.chat.id, ChatPermissions(can_send_messages=True, can_send_media_messages=True))
       return await eod(message, lock_msg3)
    await eod(message, lock_msg4)

back_button = types.InlineKeyboardMarkup(
            [[
             types.InlineKeyboardButton(b_button,callback_data="B_LO"),
             ]]
             )

@bot.on_callback_query(filters.regex('^b_locks'))
async def b_mute(client, callback_query):
    if callback_query.from_user.id != it_s6.me.id:
       return await bot.answer_callback_query(callback_query.id, text=c_me, show_alert=True)
    return await callback_query.edit_message_text(
        strings.HELP_CMD.format(module=__mod_name__, help=__help__),
        reply_markup=back_button)

@bot.on_callback_query(filters.regex('^B_LO'))
async def B_1(client, callback_query):
    if callback_query.from_user.id != it_s6.me.id:
       return await bot.answer_callback_query(callback_query.id, text=c_me, show_alert=True)
    return await callback_query.edit_message_text(
        text="", 
        reply_markup=MENU, 
        parse_mode=enums.ParseMode.MARKDOWN
    )

__mod_name__ = "Locks"  
    
__help__ = f"""  

{SORUCE_EMJ} `{HNDLR}{lock_command}`
{lock_command_us}

{SORUCE_EMJ} `{HNDLR}{unlock_command}`
{unlock_command_us}

{My_User}
"""
    
    
string = {"module": __mod_name__, "help": __help__}   
MODULE.append(string)