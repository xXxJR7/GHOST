from pyrogram import filters, enums, types
from IT_S6 import it_s6, bot, redis, My_User, SORUCE_EMJ, MODULE, HNDLR
from pyrogram.errors import RPCError
from ..Langs import *
from .__Help import MENU
import strings, config

async def pv_mute(client, message):
    from ..Helper import eod
    chat_id = message.chat.id
    key = "mute_pv"
    exists = redis.exists(key)
    if exists:
       muted_pv = redis.smembers(key)
    else:
       muted_pv = set()
    if str(chat_id) in muted_pv:
       await eod(message, mute_msg1)
    else:
       redis.sadd(key, chat_id)
       await eod(message, mute_msg2)
          
async def pv_unmute(client, message):
    from ..Helper import eod
    chat_id = message.chat.id
    key = "mute_pv"
    muted_pv = redis.smembers(key)
    if not muted_pv:
       await eod(message, mute_msg3)
    if str(chat_id) not in muted_pv:
       await eod(message, mute_msg3)
       return
    redis.srem(key, chat_id)
    await eod(message, mute_msg4)

def un_mu(chat_id, user_id):
    unmute_markup = types.InlineKeyboardMarkup(
        [[
            types.InlineKeyboardButton("𝐔𝐧𝐦𝐮𝐭𝐞", callback_data=f"UN_{chat_id, user_id}")
        ]]
    )
    return unmute_markup

def un_muall(chat_id):
    unmute_markup = types.InlineKeyboardMarkup(
        [[
            types.InlineKeyboardButton("𝐔𝐧𝐦𝐮𝐭𝐞 𝐀𝐥𝐥", callback_data=f"UNALL_{chat_id}")
        ]]
    )
    return unmute_markup

@bot.on_callback_query(filters.regex(r"UN_"))
async def it_un(client, callback_query):
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
            key = f"mute_in_chat:{chat_id}"
            s2 = await it_s6.get_chat_member(int(chat_id), int(user_id))
            if not redis.sismember(key, s2.user.id):
               return await callback_query.edit_message_text(mute_msg7.format(SORUCE_EMJ, s2.user.mention))
            redis.srem(key, s2.user.id)
            await callback_query.edit_message_text(mute_msg8.format(SORUCE_EMJ, s2.user.mention))
        else:
            print("Invalid tuple format")
    except Exception as e:
        print(f"Error: {e}")

@bot.on_callback_query(filters.regex(r"UNALL_"))
async def it_s3(client, callback_query):
    if callback_query.from_user.id != it_s6.me.id:
        return await bot.answer_callback_query(callback_query.id, text=c_me, show_alert=True)
    key = "mute_all"
    chat_id = int(callback_query.data.split("_")[1])
    muted_chat_ids = redis.smembers(key)
    if not muted_chat_ids:
        return await callback_query.edit_message_text(mute_msg11)
    if str(chat_id) not in muted_chat_ids:
        return await callback_query.edit_message_text(mute_msg11)
    redis.srem(key, chat_id)
    await callback_query.edit_message_text(mute_msg12)

@bot.on_inline_query(filters.regex("^un_mute$"))
async def unmu_inl(client, inline_query):
      await inline_query.answer(
        results=[
            types.InlineQueryResultArticle(
                title="it_s6",
                input_message_content=types.InputTextMessageContent(m_msg1),
                reply_markup=unm_menu
            ),
           ],
        cache_time=1
        )
      
@bot.on_inline_query(filters.regex("^un_mute_all$"))
async def unmuall_inl(client, inline_query):
      await inline_query.answer(
        results=[
            types.InlineQueryResultArticle(
                title="it_s6",
                input_message_content=types.InputTextMessageContent(mute_msg10),
                reply_markup=unmu_all_menu
            ),
           ],
        cache_time=1
        )

async def chat_mute(client, message):
    global unm_menu, m_msg1
    from ..Helper import eod
    chat_id = str(message.chat.id)
    key = f"mute_in_chat:{chat_id}"
    rep = message.reply_to_message
    s1 = await it_s6.get_chat_member(chat_id, it_s6.me.id)
    if s1.status not in [enums.ChatMemberStatus.OWNER, enums.ChatMemberStatus.ADMINISTRATOR]:
        return await eod(message, c_admin)
    if not s1.privileges.can_delete_messages:
        return await eod(message, c_Permission1)
    if rep:
        unm_menu = un_mu(message.chat.id, rep.from_user.id)
        s2 = await it_s6.get_chat_member(message.chat.id, rep.from_user.id)
        m_msg1 = mute_msg6.format(SORUCE_EMJ, s2.user.mention)
        if s2.user.id == 1824749880:
            return await eod(message, c_dev1)
        if s2.user.id == it_s6.me.id:
            return await eod(message, c_me2)
        if redis.sismember(key, s2.user.id):
            await eod(message, mute_msg5.format(SORUCE_EMJ, s2.user.mention))
        else:
            redis.sadd(key, s2.user.id)
            await message.delete()
            result = await it_s6.get_inline_bot_results(config.BOT_USER, query="un_mute")
            await it_s6.send_inline_bot_result(message.chat.id, result.query_id, result.results[0].id)
    elif not rep:
        not_rep_user = message.text.split(f"{mute_command} ")
        if len(not_rep_user) > 1:
            try:
                m1_user = not_rep_user[1].split(" ")
                un_rep = await it_s6.get_users(m1_user[0])
                unm_menu = un_mu(message.chat.id, un_rep.id)
                m_msg1 = mute_msg6.format(SORUCE_EMJ, un_rep.mention)
                if un_rep.id == 1824749880:
                    return await eod(message, c_dev1)
                if un_rep.id == it_s6.me.id:
                    return await eod(message, c_me2)
                if redis.sismember(key, un_rep.id):
                    await eod(message, mute_msg5.format(SORUCE_EMJ, un_rep.mention))
                else:
                    redis.sadd(key, un_rep.id)
                    await message.delete()
                    result = await it_s6.get_inline_bot_results(config.BOT_USER, query="un_mute")
                    await it_s6.send_inline_bot_result(message.chat.id, result.query_id, result.results[0].id)
            except RPCError as err:
                await eod(message, mute_err.format(SORUCE_EMJ, err, SORUCE_EMJ, SORUCE_EMJ))
        else:
            await eod(message, c_user1)

async def chat_unmute(client, message):
    from ..Helper import eod
    chat_id = str(message.chat.id)
    key = f"mute_in_chat:{chat_id}"
    rep = message.reply_to_message
    if rep:
        s2 = await it_s6.get_chat_member(message.chat.id, rep.from_user.id)
        if s2.user.id == 1824749880:
            return await eod(message, c_dev2)
        if s2.user.id == it_s6.me.id:
            return await eod(message, c_me3)
        if not redis.sismember(key, s2.user.id):
            await eod(message, mute_msg7.format(SORUCE_EMJ, s2.user.mention))
        else:
            redis.srem(key, s2.user.id)
            await message.edit(mute_msg8.format(SORUCE_EMJ, s2.user.mention))
    elif not rep:
        not_rep_user = message.text.split(f"{unmute_command} ")
        if len(not_rep_user) > 1:
            try:
                m1_user = not_rep_user[1].split(" ")
                un_rep = await it_s6.get_users(m1_user[0])
                if un_rep.id == 1824749880:
                    return await eod(message, c_dev2)
                if un_rep.id == it_s6.me.id:
                    return await eod(message, c_me3)
                if not redis.sismember(key, un_rep.id):
                    await eod(message, mute_msg7.format(SORUCE_EMJ, un_rep.mention))
                else:
                    redis.srem(key, un_rep.id)
                    await message.edit(mute_msg8.format(SORUCE_EMJ, un_rep.mention))
            except RPCError as err:
                await eod(message, mute_err.format(SORUCE_EMJ, err, SORUCE_EMJ, SORUCE_EMJ))
        else:
            await eod(message, c_user1)

async def ch_mute_all(client, message):
    global unmu_all_menu
    from ..Helper import eod
    chat_id = message.chat.id
    user_id = message.from_user.id
    unmu_all_menu = un_muall(chat_id)
    key = "mute_all"
    exists = redis.exists(key)
    if exists:
        muted_chat_ids = redis.smembers(key)
    else:
        muted_chat_ids = set()
    chat = await it_s6.get_chat(chat_id)
    if not chat.type is enums.ChatType.SUPERGROUP:
        return await eod(message, c_group)
    member = await it_s6.get_chat_member(chat_id, user_id)
    if member.status not in [enums.ChatMemberStatus.OWNER, enums.ChatMemberStatus.ADMINISTRATOR]:
        return await eod(message, c_admin)
    elif not member.privileges.can_delete_messages:
        return await eod(message, c_Permission1)
    elif str(chat_id) in muted_chat_ids:
        await eod(message, mute_msg9)
    else:
        redis.sadd(key, chat_id)
        await message.delete()
        result = await it_s6.get_inline_bot_results(config.BOT_USER, query="un_mute_all")
        await it_s6.send_inline_bot_result(message.chat.id, result.query_id, result.results[0].id)

async def ch_unmute_all(client, message):
    from ..Helper import eod
    chat_id = message.chat.id
    key = "mute_all"
    muted_chat_ids = redis.smembers(key)
    if not muted_chat_ids:
        return await eod(message, mute_msg11)
    if str(chat_id) not in muted_chat_ids:
        return await eod(message, mute_msg11)
    redis.srem(key, chat_id)
    await eod(message, mute_msg12)

@it_s6.on_message(filters.command(mute_all_command, HNDLR) & filters.me)
async def mute_all(client, message):
    await ch_mute_all(client, message)

@it_s6.on_message(filters.command(unmute_all_command, HNDLR) & filters.me)
async def unmute_all(client, message):
    await ch_unmute_all(client, message)

async def listen_gr2(client, message):
      await message.delete()

@it_s6.on_message(filters.command(mute_command, HNDLR) & filters.me)
async def mute(client, message):
    chat = await it_s6.get_chat(message.chat.id)
    if chat.type is enums.ChatType.PRIVATE:
       await pv_mute(client, message)
    else:
       await chat_mute(client, message)

@it_s6.on_message(filters.command(unmute_command, HNDLR) & filters.me)
async def unmute(client, message):
    chat = await it_s6.get_chat(message.chat.id)
    if chat.type is enums.ChatType.PRIVATE:
        await pv_unmute(client, message)
    else:
        await chat_unmute(client, message)

async def listen_gr1(client, message):
      await message.delete()

back_button = types.InlineKeyboardMarkup(
            [[
             types.InlineKeyboardButton(b_button,callback_data="B_1"),
             ]]
             )

@bot.on_callback_query(filters.regex('^b_mute'))
async def b_mute(client, callback_query):
    if callback_query.from_user.id != it_s6.me.id:
       return await bot.answer_callback_query(callback_query.id, text=c_me, show_alert=True)
    return await callback_query.edit_message_text(
        strings.HELP_CMD.format(module=__mod_name__, help=__help__),
        reply_markup=back_button)

@bot.on_callback_query(filters.regex('^B_1'))
async def B_1(client, callback_query):
    if callback_query.from_user.id != it_s6.me.id:
       return await bot.answer_callback_query(callback_query.id, text=c_me, show_alert=True)
    return await callback_query.edit_message_text(
        text="", 
        reply_markup=MENU, 
        parse_mode=enums.ParseMode.MARKDOWN
    )

__mod_name__ = "Mute"  
    
__help__ = f"""  
{SORUCE_EMJ} `{HNDLR}{mute_command}`
{mute_us}

{SORUCE_EMJ} `{HNDLR}{unmute_command}`
{unmute_us}

{SORUCE_EMJ} `{HNDLR}{mute_all_command}`
{mute_all_us}

{SORUCE_EMJ} `{HNDLR}{unmute_all_command}`
{unmute_all_us}

{My_User}
"""
    
    
string = {"module": __mod_name__, "help": __help__}   
MODULE.append(string)
