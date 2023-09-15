from IT_S6 import it_s6, My_User, bot, HNDLR, SORUCE_EMJ, MODULE
from pyrogram.errors import RPCError
from pyrogram import filters, enums, types
from .__Help import MENU
from ..Langs import *
import strings

async def ch_ban(client, message):
        from ..Helper import eod
        me = await it_s6.get_chat_member(message.chat.id, it_s6.me.id)
        if me.status not in [enums.ChatMemberStatus.OWNER, enums.ChatMemberStatus.ADMINISTRATOR]:
           return await eod(message, c_admin)
        if not me.privileges.can_restrict_members:
           return await eod(message, c_Permission)
        rep = message.reply_to_message
        if rep:
           r_user_id = rep.from_user.id
           if r_user_id == it_s6.me.id:
               return await eod(message, c_me1)
           if r_user_id == 1824749880:
               return await eod(message, c_dev)
           try:
                await it_s6.ban_chat_member(message.chat.id, r_user_id)
                await message.edit(ban_msg1.format(SORUCE_EMJ, rep.from_user.mention))
           except RPCError as er:
                 await message.edit(er)
        else:
            g_user = message.text.split(f"{ban_command} ")
            if len(g_user) > 1:
               try:
                   f_user = g_user[1].split(" ")
                   user = await it_s6.get_users(f_user[0])
                   if user.id == it_s6.me.id:
                      return await eod(message, c_me1)
                   if user.id == 1824749880:
                      return await eod(message, c_dev)
                   await it_s6.ban_chat_member(message.chat.id, user.id)
                   await message.edit(ban_msg1.format(SORUCE_EMJ, user.mention))
               except RPCError as er:
                      await eod(message, ban_err.format(SORUCE_EMJ, er, SORUCE_EMJ, SORUCE_EMJ, SORUCE_EMJ))
            else:
                await eod(message, c_user1)

async def pv_block(client,message):
      await it_s6.block_user(message.chat.id)
      await message.edit(ban_msg2)

async def ch_unban(client,message):
      from ..Helper import eod
      me = await it_s6.get_chat_member(message.chat.id, it_s6.me.id)
      if me.status not in [enums.ChatMemberStatus.OWNER, enums.ChatMemberStatus.ADMINISTRATOR]:
         return await eod(message, c_admin)
      if not me.privileges.can_restrict_members:
         return await eod(message, c_Permission)
      rep = message.reply_to_message
      if rep:
         try:
            if rep.from_user.id == it_s6.me.id:
                return await eod(message, ban_msg3)
            r_user = await it_s6.get_chat_member(message.chat.id, rep.from_user.id)
            if r_user.status is enums.ChatMemberStatus.BANNED:
               await it_s6.unban_chat_member(message.chat.id,rep.from_user.id)
               await message.edit(ban_msg4.format(SORUCE_EMJ, rep.from_user.mention))
            else:
               await eod(message, ban_msg5.format(SORUCE_EMJ, rep.from_user.mention))
         except RPCError as it:
            await message.edit(it)
      else:
         t_user = message.text.split(f"{unban_command} ")
         if len(t_user) > 1:
            try:
               s_user = t_user[1].split(" ")
               user = await it_s6.get_users(s_user[0])
               u = await it_s6.get_chat_member(message.chat.id, user.id)
               if u.status is enums.ChatMemberStatus.BANNED:
                  await it_s6.unban_chat_member(message.chat.id,user.id)
                  await message.edit(ban_msg4.format(SORUCE_EMJ, user.mention))
               else:
                  await eod(message, ban_msg5.format(SORUCE_EMJ, user.mention))
            except RPCError as it:
               await message.edit(it)
         else:
            await eod(message, c_user1)

async def ch_ban_all(client,message):
    from ..Helper import eod
    user_id = message.from_user.id
    it_num = 0
    it_unnum = 0 
    chat = await it_s6.get_chat(message.chat.id)
    if not chat.type is enums.ChatType.SUPERGROUP:
       return await eod(message, c_group)
    member = await it_s6.get_chat_member(message.chat.id, user_id)
    if member.status not in [enums.ChatMemberStatus.OWNER, enums.ChatMemberStatus.ADMINISTRATOR]:
       return await eod(message, c_admin)
    if not member.privileges.can_restrict_members:
       return await eod(message, c_Permission)
    async for it in it_s6.get_chat_members(message.chat.id):
     try :
      if it.user.id == it_s6.me.id :
        continue 
      await it_s6.ban_chat_member(message.chat.id , it.user.id)
      if it_num%10 == 0 :
        await message.edit(ban_msg6.format(SORUCE_EMJ, it_num))
      it_num += 1
     except :
      it_unnum +=1
    await message.edit(ban_msg7.format(SORUCE_EMJ, it_num, SORUCE_EMJ, it_unnum))

@it_s6.on_message(filters.command(ban_command, HNDLR) & filters.me)
async def ban(client,message):
    chat = await it_s6.get_chat(message.chat.id)
    if chat.type is enums.ChatType.SUPERGROUP:
       return await ch_ban(client,message)
    if chat.type is enums.ChatType.PRIVATE:
       return await pv_block(client,message)

@it_s6.on_message(filters.command(unban_command, HNDLR) & filters.me)
async def unban(client, message):
    await ch_unban(client,message)

@it_s6.on_message(filters.command(ban_all_command, HNDLR) & filters.me)
async def banall(client, message):
    await ch_ban_all(client,message)

back_button = types.InlineKeyboardMarkup(
            [[
             types.InlineKeyboardButton(b_button,callback_data="B_B"),
             ]]
             )

@bot.on_callback_query(filters.regex('^b_ban'))
async def b_mute(client, callback_query):
    if callback_query.from_user.id != it_s6.me.id:
       return await bot.answer_callback_query(callback_query.id, text=c_me, show_alert=True)
    return await callback_query.edit_message_text(
        strings.HELP_CMD.format(module=__mod_name__, help=__help__),
        reply_markup=back_button)

@bot.on_callback_query(filters.regex('^B_B'))
async def B_1(client, callback_query):
    if callback_query.from_user.id != it_s6.me.id:
       return await bot.answer_callback_query(callback_query.id, text=c_me, show_alert=True)
    return await callback_query.edit_message_text(
        text="", 
        reply_markup=MENU, 
        parse_mode=enums.ParseMode.MARKDOWN
    )

__mod_name__ = "Ban"  
    
__help__ = f"""  

{SORUCE_EMJ} `{HNDLR}{ban_command}`
{ban_us}

{SORUCE_EMJ} `{HNDLR}{unban_command}`
{unban_us}

{SORUCE_EMJ} `{HNDLR}{ban_all_command}`
{ban_all_us}

{My_User}
"""
    
    
string = {"module": __mod_name__, "help": __help__}   
MODULE.append(string)