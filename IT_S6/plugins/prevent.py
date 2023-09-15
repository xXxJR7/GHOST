from IT_S6 import it_s6, bot, redis, My_User, HNDLR, SORUCE_EMJ, MODULE, LANG
from pyrogram import filters, enums, types
from ..Langs import *
from .__Help import R_MENU
import strings, config

@it_s6.on_message(filters.command(prevent_word_command, HNDLR) & filters.group & filters.me)
async def prevent_word(client, message):
    from ..Helper import eod
    get_word = message.text.split(" ")
    if len(get_word) < 2:
        return await eod(message, c_command)
    word = get_word[1].split(" ")
    c_me = await it_s6.get_chat_member(message.chat.id, it_s6.me.id)
    if c_me.status not in [enums.ChatMemberStatus.OWNER, enums.ChatMemberStatus.ADMINISTRATOR]:
       return await eod(message, c_admin)
    if word[0] == prevent_word_command1:
       if str(message.chat.id) in redis.smembers("Prevent_Userbot"):
          return await eod(message, prevent_msg1)
       redis.sadd("Prevent_Userbot", message.chat.id)
       await eod(message, prevent_msg2)
    if word[0] == prevent_word_command2:
       if str(message.chat.id) in redis.smembers("Prevent_Ban"):
          return await eod(message, prevent_msg3)
       redis.sadd("Prevent_Ban", message.chat.id)
       await eod(message, prevent_msg4)
    c_words = redis.smembers(f"Forbidden_Words {message.chat.id}")
    if word[0] not in c_words:
       redis.sadd(f"Forbidden_Words {message.chat.id}", word[0])
       return await eod(message, prevent_msg5)
    await eod(message, prevent_msg6)

@it_s6.on_message(filters.command(unprevent_word_command, HNDLR) & filters.group & filters.me)
async def unprevent_word(client, message):
    from ..Helper import eod
    get_word = message.text.split(f"{unprevent_word_command} ")
    if len(get_word) < 2:
        return await eod(message, c_command)
    word = get_word[1].split(" ")
    if word[0] == prevent_word_command1:
       if str(message.chat.id) not in redis.smembers("Prevent_Userbot"):
          return await eod(message, prevent_msg7)
       redis.srem("Prevent_Userbot", message.chat.id)
       await eod(message, prevent_msg8)
    if word[0] == prevent_word_command2:
       if str(message.chat.id) not in redis.smembers("Prevent_Ban"):
          return await eod(message, prevent_msg9)
       redis.srem("Prevent_Ban", message.chat.id)
       await eod(message, prevent_msg10)
    c_words = redis.smembers(f"Forbidden_Words {message.chat.id}")
    if word[0] in c_words:
       redis.srem(f"Forbidden_Words {message.chat.id}", word[0])
       return await eod(message, prevent_msg11)
    await eod(message, prevent_msg12)

def un_m(chat_id, user_id):
    unmute_markup = types.InlineKeyboardMarkup(
        [[
            types.InlineKeyboardButton("Unmute", callback_data=f"U_{chat_id, user_id}")
        ]]
    )
    return unmute_markup

@bot.on_callback_query(filters.regex(r"U_"))
async def it_u(client, callback_query):
    if callback_query.from_user.id != it_s6.me.id:
        return await bot.answer_callback_query(callback_query.id, text=c_me, show_alert=True)
    
    data_parts = callback_query.data.split("_")
    if len(data_parts) < 2:
        return
    ids_tuple_str = data_parts[1]
    try:
        ids_tuple = eval(ids_tuple_str)
        if isinstance(ids_tuple, tuple) and len(ids_tuple) == 2:
            chat_id, user_id = ids_tuple
            await it_s6.unban_chat_member(int(chat_id), int(user_id))
            await callback_query.edit_message_text(mute_msg4)
        else:
            print("Invalid tuple format")
    except Exception as e:
        print(f"Error: {e}")

@bot.on_inline_query(filters.regex("^unmute$"))
async def un_inl(client, inline_query):
      await inline_query.answer(
        results=[
            types.InlineQueryResultArticle(
                title="it_s6",
                input_message_content=types.InputTextMessageContent(m_msg),
                reply_markup=unm_menu
            ),
           ],
        cache_time=1
        )

async def Forbidden_Words_ls(client, message):
    global unm_menu, m_msg
    unm_menu = un_m(message.chat.id, message.from_user.id)
    c_words = redis.smembers(f"Forbidden_Words {message.chat.id}")
    if c_words is not None:
        for word in c_words:
            if word in message.text and is not None:
                warn_Numbers = redis.hget("Forbidden_Words_Numbers", message.from_user.id)
                if warn_Numbers is None:
                    warn_Numbers = 2
                else:
                    warn_Numbers = int(warn_Numbers)
                if warn_Numbers == 1:
                    redis.hdel("Forbidden_Words_Numbers", message.from_user.id)
                    try:
                        m_msg = prevent_msg13.format(SORUCE_EMJ, message.from_user.mention, SORUCE_EMJ, SORUCE_EMJ)
                        await message.delete() 
                        await it_s6.restrict_chat_member(message.chat.id, message.from_user.id, types.ChatPermissions(can_send_messages=False, can_send_media_messages=False))
                        result = await it_s6.get_inline_bot_results(config.BOT_USER, query="unmute")
                        await it_s6.send_inline_bot_result(message.chat.id, result.query_id, result.results[0].id)
                    except:
                        pass
                else:
                    warn_Numbers -= 1
                    redis.hset("Forbidden_Words_Numbers", message.from_user.id, warn_Numbers)
                    try:
                        await message.delete()
                        await message.reply(prevent_msg14.format(SORUCE_EMJ, message.from_user.mention, SORUCE_EMJ, SORUCE_EMJ, warn_Numbers))
                    except :
                        pass

async def preventuserbot_ls(client, message):
    if message.text.startswith("."):
        try:
           await message.delete()
        except:
           pass
        Userbot_Numbers = redis.hget("Userbot_Numbers", message.from_user.id)
        if Userbot_Numbers is None:
           Userbot_Numbers = 4
        else:
           Userbot_Numbers = int(Userbot_Numbers)
        if Userbot_Numbers == 1:
           redis.hdel("Userbot_Numbers", message.from_user.id)
           await it_s6.restrict_chat_member(message.chat.id, message.from_user.id, types.ChatPermissions(can_send_messages=False, can_send_media_messages=False))
           await it_s6.send_message(message.chat.id ,prevent_msg15.format(SORUCE_EMJ, message.from_user.mention, SORUCE_EMJ, SORUCE_EMJ))
        else:
           Userbot_Numbers -= 1
           redis.hset("Userbot_Numbers", message.from_user.id, Userbot_Numbers)
           await message.reply(prevent_msg16.format(SORUCE_EMJ, message.from_user.mention, SORUCE_EMJ, SORUCE_EMJ, SORUCE_EMJ, Userbot_Numbers))
           
rights = types.ChatPrivileges(
            can_manage_chat=False,
            can_delete_messages=False,
            can_manage_video_chats=False,
            can_restrict_members=False,
            can_promote_members=False,
            can_change_info=False,
            can_post_messages=False,
            can_edit_messages=False,
            can_invite_users=False,
            can_pin_messages=False
            )

data = {"users": {}}

@it_s6.on_message(filters.left_chat_member & filters.create(lambda it, s6, message: str(message.chat.id) in redis.smembers("Prevent_Ban")) & ~filters.me)
async def preventban_ls(client, message):
    if message.from_user:
     id = str(message.from_user.id)
     users = data["users"]
     if id not in users:
        users[id] = {"numbers" : 3}
     for i in users:
         if i == id:
            users[id]["numbers"] -= 1
     ban_numbers = users[id]["numbers"]
     if ban_numbers == 0:
        await it_s6.ban_chat_member(message.chat.id, message.from_user.id)
        await it_s6.send_message(message.chat.id, prevent_msg17.format(SORUCE_EMJ, message.from_user.mention, SORUCE_EMJ))
        users.pop(id)

back_button = types.InlineKeyboardMarkup(
            [[
             types.InlineKeyboardButton(b_button,callback_data="B_prev"),
             ]]
             )

@bot.on_callback_query(filters.regex('^b_prevent'))
async def b_prevent(client, callback_query):
    if callback_query.from_user.id != it_s6.me.id:
       return await bot.answer_callback_query(callback_query.id, text=c_me, show_alert=True)
    return await callback_query.edit_message_text(
        strings.HELP_CMD.format(module=__mod_name__, help=__help__),
        reply_markup=back_button)

@bot.on_callback_query(filters.regex('^B_prev'))
async def B_prev(client, callback_query):
    if callback_query.from_user.id != it_s6.me.id:
       return await bot.answer_callback_query(callback_query.id, text=c_me, show_alert=True)
    return await callback_query.edit_message_text(
        text="", 
        reply_markup=R_MENU, 
        parse_mode=enums.ParseMode.MARKDOWN
    )

__mod_name__ = "Prevent"  
    
__help__ = f"""  

{SORUCE_EMJ} `{HNDLR}{prevent_word_command} {prevent_word_command1}`
{prevent_us1}

{SORUCE_EMJ} `{HNDLR}{prevent_word_command} {prevent_word_command2}`
{prevent_us2}

{SORUCE_EMJ} `{HNDLR}{prevent_word_command} + {prevent_word_command3}`
{prevent_us3}

{SORUCE_EMJ} `{HNDLR}{unprevent_word_command} {prevent_word_command1}`
{SORUCE_EMJ} `{HNDLR}{unprevent_word_command} {prevent_word_command2}`
{SORUCE_EMJ} `{HNDLR}{unprevent_word_command} + {prevent_word_command3}`

{My_User}
"""
    
    
string = {"module": __mod_name__, "help": __help__}   
MODULE.append(string)
