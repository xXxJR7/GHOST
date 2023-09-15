from IT_S6 import it_s6, bot, redis, My_User, SORUCE_EMJ, HNDLR, MODULE, LOG
from pyrogram import filters, types, enums
from ..Langs import *
from .__Help import MENU
import config, strings

def pm_menu1(chat_id):
    pm1_markup = types.InlineKeyboardMarkup(
        [[
            types.InlineKeyboardButton("Approve", callback_data=f"c1_{chat_id}"),
            types.InlineKeyboardButton("Mute", callback_data=f"c2_{chat_id}"),
        ]]
    )
    return pm1_markup

def pm_menu2(chat_id):
    pm2_markup = types.InlineKeyboardMarkup(
        [[
            types.InlineKeyboardButton("Approve", callback_data=f"c3_{chat_id}"),
            types.InlineKeyboardButton("UnMute", callback_data=f"c4_{chat_id}"),
        ]]
    )
    return pm2_markup

@it_s6.on_message(filters.command(start_pm_command, HNDLR) & filters.me)
async def start_pm(client, message):
    from ..Helper import eod
    if not redis.exists("s_pm"):
        redis.set("s_pm", "True")
        await eod(message, PMSecurity_msg1)
    else:
        await eod(message, PMSecurity_msg2)

@it_s6.on_message(filters.command(stop_pm_command, HNDLR) & filters.me)
async def stop_pm(client, message):
    from ..Helper import eod
    if not redis.exists("s_pm"):
      await eod(message, PMSecurity_msg3)
    else:
      redis.delete("s_pm")
      await eod(message, PMSecurity_msg4)

@it_s6.on_message(filters.command(a_command, HNDLR) & filters.me)
async def apr_(client, message):
    from ..Helper import eod
    chat = await it_s6.get_chat(message.chat.id)
    if not chat.type is enums.ChatType.PRIVATE:
       return await eod(message, c_pv)
    key = "Approved"
    if redis.sismember(key, message.chat.id):
       return await eod(message, PMSecurity_msg5)
    redis.sadd(key, message.chat.id)
    await eod(message, PMSecurity_msg6)

@it_s6.on_message(filters.command(d_command, HNDLR) & filters.me)
async def dis_(client, message):
    from ..Helper import eod
    chat = await it_s6.get_chat(message.chat.id)
    if not chat.type is enums.ChatType.PRIVATE:
       return await eod(message, c_pv)
    key = "Approved"
    if not redis.sismember(key, message.chat.id):
        return await eod(message, PMSecurity_msg7)
    redis.srem(key, message.chat.id)
    await eod(message, PMSecurity_msg8)

@bot.on_callback_query(filters.regex(r"c1_"))
async def it_s1(client, callback_query):
    from ..Helper import sod
    if callback_query.from_user.id != it_s6.me.id:
        return await bot.answer_callback_query(callback_query.id, text=c_me, show_alert=True)
    key = "Approved"
    chat_id = int(callback_query.data.split("_")[1])
    last_warn_msg_ids = redis.hget('last_warn_msg_ids', chat_id)
    warn_number = redis.hget('users_warns', chat_id)
    if warn_number is None:
       redis.sadd(key, chat_id)
       await it_s6.delete_messages(chat_id, int(last_warn_msg_ids))
       return await sod(chat_id, PMSecurity_msg6)
    redis.hdel('users_warns', chat_id)
    redis.sadd(key, chat_id)
    await it_s6.delete_messages(chat_id, int(last_warn_msg_ids))
    await sod(chat_id, PMSecurity_msg6)

@bot.on_callback_query(filters.regex(r"c2_"))
async def it_s2(client, callback_query):
    if callback_query.from_user.id != it_s6.me.id:
        return await bot.answer_callback_query(callback_query.id, text=c_me, show_alert=True)
    chat_id = callback_query.data.split("_")[1]
    key = "mute_pv"
    exists = redis.exists(key)
    if not exists:
       muted_pv = redis.smembers(key)
    else:
       muted_pv = set()
    if str(chat_id) in muted_pv:
       return await callback_query.edit_message_text(PMSecurity_msg9.format(wel_msg, SORUCE_EMJ), reply_markup=a_u_menu)
    redis.sadd(key, chat_id)
    await callback_query.edit_message_text(PMSecurity_msg10.format(wel_msg, SORUCE_EMJ), reply_markup=a_u_menu)

@bot.on_callback_query(filters.regex(r"c3_"))
async def it_s3(client, callback_query):
    from ..Helper import sod
    if callback_query.from_user.id != it_s6.me.id:
        return await bot.answer_callback_query(callback_query.id, text=c_me, show_alert=True)
    key = "Approved"
    chat_id = int(callback_query.data.split("_")[1])
    last_warn_msg_ids = redis.hget('last_warn_msg_ids', chat_id)
    exists = redis.smembers("mute_pv")
    warn_number = redis.hget('users_warns', chat_id)
    if str(chat_id) not in exists:
       if warn_number is None:
          redis.sadd(key, chat_id)
          await it_s6.delete_messages(chat_id, int(last_warn_msg_ids))
          return await sod(chat_id, PMSecurity_msg6)
    redis.srem("mute_pv", chat_id)
    redis.hdel('users_warns', chat_id)
    redis.sadd(key, chat_id)
    await it_s6.delete_messages(chat_id, int(last_warn_msg_ids))
    await sod(chat_id, PMSecurity_msg6)

@bot.on_callback_query(filters.regex(r"c4_"))
async def it_s4(client, callback_query):
    if callback_query.from_user.id != it_s6.me.id:
        return await bot.answer_callback_query(callback_query.id, text=c_me, show_alert=True)
    chat_id = int(callback_query.data.split("_")[1])
    key = "mute_pv"
    muted_pv = redis.smembers(key)
    if not muted_pv:
       await callback_query.edit_message_text(PMSecurity_msg11.format(wel_msg, SORUCE_EMJ), reply_markup=a_b_menu)
    if str(chat_id) not in muted_pv:
       return await callback_query.edit_message_text(PMSecurity_msg11.format(wel_msg, SORUCE_EMJ), reply_markup=a_b_menu)
    redis.srem(key, chat_id)
    await callback_query.edit_message_text(PMSecurity_msg12.format(wel_msg, SORUCE_EMJ), reply_markup=a_b_menu)

pm_photo_url = redis.get("PM_PIC")
thumb_url = redis.get("PM_PIC1")

@bot.on_inline_query(filters.regex("^sec_in$"))
async def pm_inl(client, inline_query):
    if pm_photo_url.endswith("jpg"):
       await inline_query.answer(
           results=[
            types.InlineQueryResultPhoto(
                photo_url=pm_photo_url,
                photo_width=1000,
                photo_height=1000,
                title="it_s6",
                description="",
                caption=wel_msg,
                reply_markup=a_b_menu
            ),
           ],
        cache_time=1
        )
    if pm_photo_url.endswith("mp4"):
       await inline_query.answer(
           results=[
            types.InlineQueryResultVideo(
                video_url=pm_photo_url,
                thumb_url=thumb_url,
                video_width=1000,
                video_height=1000,
                title="it_s6",
                description="",
                caption=wel_msg,
                reply_markup=a_b_menu
            ),
           ],
        cache_time=1
        )
    else:
      await inline_query.answer(
        results=[
            types.InlineQueryResultArticle(
                title="it_s6",
                input_message_content=types.InputTextMessageContent(wel_msg),
                reply_markup=a_b_menu
            ),
           ],
        cache_time=1
        )

async def pm_func(client, message):
   global wel_msg, a_b_menu, a_u_menu
   user_id = message.from_user.id
   w_numbers = 5
   warn_key = 'users_warns'
   warn_number = redis.hget(warn_key, user_id)
   a_b_menu = pm_menu1(message.chat.id)
   a_u_menu = pm_menu2(message.chat.id)
   key = "Approved"
   exists = redis.sismember(key, user_id)
   if not exists:
    me = await it_s6.get_me()
    if warn_number is None:
        warn_number = 6
    else:
        warn_number = int(warn_number)
    if warn_number == 1:
        last_warn_msg_id = redis.hget('last_warn_msg_ids', user_id)
        if last_warn_msg_id:
            try:
                await it_s6.delete_messages(user_id, int(last_warn_msg_id))
            except Exception as e:
                print(f"Failed to delete previous warning message: {e}")

        key = "mute_pv"
        exists = redis.exists(key)
        if exists:
           muted_pv = redis.smembers(key)
        else:
           muted_pv = set()
        if str(user_id) in muted_pv:
           return
        redis.sadd(key, user_id)
        await message.reply(PMSecurity_msg13)
        redis.hdel(warn_key, user_id)
    else:
        s = await it_s6.get_users(user_id)
        mention = s.mention
        warn_number -= 1
        redis.hset(warn_key, user_id, warn_number)

        last_warn_msg_id = redis.hget('last_warn_msg_ids', user_id)
        if last_warn_msg_id:
            try:
                await it_s6.delete_messages(user_id, int(last_warn_msg_id))
            except Exception as e:
                print(f"Failed to delete previous warning message: {e}")
        wel_msg = PMSecurity_msg14.format(SORUCE_EMJ, me.first_name, SORUCE_EMJ, mention, SORUCE_EMJ, SORUCE_EMJ, SORUCE_EMJ, warn_number, w_numbers)
        result = await it_s6.get_inline_bot_results(config.BOT_USER, query="sec_in")
        sent_message = await it_s6.send_inline_bot_result(message.chat.id, result.query_id, result.results[0].id)
        message_id = sent_message.updates[0].id
        redis.hset('last_warn_msg_ids', user_id, message_id)

@it_s6.on_message(filters.private & ~ filters.me & ~ filters.bot)
async def lis_incoming(client, message):
   if redis.get("s_log") is not None and "True" in redis.get("s_log"):
      await it_s6.forward_messages(int(LOG), message.chat.id, message.id)
   if str(message.chat.id) in redis.smembers("mute_pv"):
      return await message.delete()
   if redis.get("s_pm") is not None and "True" in redis.get("s_pm"):
      await pm_func(client, message)

back_button = types.InlineKeyboardMarkup(
            [[
             types.InlineKeyboardButton(b_button,callback_data="B_PM"),
             ]]
             )

@bot.on_callback_query(filters.regex('^b_PMSecurity'))
async def b_PMSecurity(client, callback_query):
    if callback_query.from_user.id != it_s6.me.id:
       return await bot.answer_callback_query(callback_query.id, text=c_me, show_alert=True)
    return await callback_query.edit_message_text(
        strings.HELP_CMD.format(module=__mod_name__, help=__help__),
        reply_markup=back_button)

@bot.on_callback_query(filters.regex('^B_PM'))
async def B_PM(client, callback_query):
    if callback_query.from_user.id != it_s6.me.id:
       return await bot.answer_callback_query(callback_query.id, text=c_me, show_alert=True)
    return await callback_query.edit_message_text(
        text="", 
        reply_markup=MENU, 
        parse_mode=enums.ParseMode.MARKDOWN
    )

__mod_name__ = "PMSecurity"  
    
__help__ = f"""  

{SORUCE_EMJ} `{HNDLR}{start_pm_command}`
{start_pm_us}

{SORUCE_EMJ} `{HNDLR}{stop_pm_command}`
{stop_pm_us}

{SORUCE_EMJ} `{HNDLR}{a_command}`
{a_us}

{SORUCE_EMJ} `{HNDLR}{d_command}`
{d_us}

{My_User}
"""
    
    
string = {"module": __mod_name__, "help": __help__}   
MODULE.append(string)