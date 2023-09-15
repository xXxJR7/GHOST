from pyrogram import filters, types, enums
from IT_S6 import it_s6, My_User, bot, HNDLR, SORUCE_EMJ, MODULE
from asyncio import sleep
from .__Help import MENU
from ..Langs import *
import strings

@it_s6.on_message(filters.command(id_command, HNDLR) & filters.me)
async def get_info(client,message):
  rep = message.reply_to_message
  if rep :
    if rep.sender_chat :
       ch_id = rep.sender_chat.id
       await message.edit(id_msg1.format(SORUCE_EMJ, ch_id))
    if rep.from_user.username :
       username = f"@{rep.from_user.username}"
    else :
      username = id_nofound
    ge_user = await it_s6.get_chat(rep.from_user.id)
    if ge_user.bio :
       bio = f"{ge_user.bio}"
    else :
       bio = id_nofound
    h_info = id_msg2.format(SORUCE_EMJ, ge_user.first_name, SORUCE_EMJ, username, SORUCE_EMJ, ge_user.id, SORUCE_EMJ, message.chat.id, SORUCE_EMJ, bio)
    if rep.from_user.photo :
      await message.delete()
      async for photo in it_s6.get_chat_photos(rep.from_user.id):
        await message.reply_photo(photo.file_id,caption=h_info)
        break 
    else :
      await message.edit(h_info)
  else :
    not_rep_user = message.text.split(" ")
    if len(not_rep_user) > 1:
         m1_user = not_rep_user[1].split(" ")
         un_rep = await client.get_users(m1_user[0])
         await sleep(0.3)
         ge_un_rep_user = await it_s6.get_chat(un_rep.id)
         if ge_un_rep_user.username :
            username = f"@{ge_un_rep_user.username}"
         else:
            username = id_nofound
         if ge_un_rep_user.bio :
            bio = f"{ge_un_rep_user.bio}"
         else:
            bio = id_nofound
         h1_info = id_msg2.format(SORUCE_EMJ, ge_un_rep_user.first_name, SORUCE_EMJ, username, SORUCE_EMJ, ge_un_rep_user.id, SORUCE_EMJ, message.chat.id, SORUCE_EMJ, bio)
         if un_rep.photo :
            await message.delete()
            async for photo in it_s6.get_chat_photos(ge_un_rep_user.id):
               await message.reply_photo(photo.file_id,caption=h1_info)
               break
         else:
            await message.edit(h1_info)
    else:
       ge_user = await it_s6.get_chat("me")
       if ge_user.bio :
         bio = f"{ge_user.bio}"
       else :
         bio = id_nofound
       if ge_user.username :
         username = f"@{ge_user.username}"
       else :
         username = id_nofound
       m_info = id_msg3.format(SORUCE_EMJ, ge_user.first_name, SORUCE_EMJ, username, SORUCE_EMJ, ge_user.id, SORUCE_EMJ, message.chat.id, SORUCE_EMJ, bio)
       if message.from_user.photo :
         await message.delete()
         async for photo in it_s6.get_chat_photos(message.from_user.id):
           await message.reply_photo(photo.file_id,caption=m_info)
           break 
       else :
         await message.edit(m_info)

back_button = types.InlineKeyboardMarkup(
            [[
             types.InlineKeyboardButton(b_button,callback_data="B_I"),
             ]]
             )

@bot.on_callback_query(filters.regex('^b_id'))
async def b_mute(client, callback_query):
    if callback_query.from_user.id != it_s6.me.id:
       return await bot.answer_callback_query(callback_query.id, text=c_me, show_alert=True)
    return await callback_query.edit_message_text(
        strings.HELP_CMD.format(module=__mod_name__, help=__help__),
        reply_markup=back_button)

@bot.on_callback_query(filters.regex('^B_I'))
async def B_1(client, callback_query):
    if callback_query.from_user.id != it_s6.me.id:
       return await bot.answer_callback_query(callback_query.id, text=c_me, show_alert=True)
    return await callback_query.edit_message_text(
        text="", 
        reply_markup=MENU, 
        parse_mode=enums.ParseMode.MARKDOWN
    )

__mod_name__ = "Id"  
    
__help__ = f"""  

{SORUCE_EMJ} `{HNDLR}{id_command}`
{id_us}

{My_User}
"""
    
string = {"module": __mod_name__, "help": __help__}   
MODULE.append(string)