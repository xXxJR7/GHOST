from IT_S6 import it_s6, bot, redis, My_User, SORUCE_EMJ, HNDLR, MODULE
from pyrogram import filters, enums, types
from pyrogram.errors import UserNotParticipant
from .__Help import MENU
from ..Langs import *
import strings, config

@it_s6.on_message(filters.command(must_join_command, HNDLR) & filters.me)
async def must_join(client,message):
    from ..Helper import eod
    get_channel = message.text.split(f"{must_join_command} ")
    if len(get_channel) < 2:
        return await eod(message, must_msg1)
    channel = get_channel[1].split(" ")
    if channel[0].startswith("@"):
        return await eod(message, must_msg2)
    if channel[0].startswith("https://"):
        return await eod(message, must_msg2)
    try:
        Name_Channel = (await bot.get_chat(channel[0])).title
    except:
        pass
    try:
       c_me = await it_s6.get_chat_member(channel[0], it_s6.me.id)
    except:
       return await eod(message, must_msg3.format(SORUCE_EMJ, SORUCE_EMJ, channel[0]))
    if c_me.status not in [enums.ChatMemberStatus.OWNER, enums.ChatMemberStatus.ADMINISTRATOR]:
       return await eod(message, must_msg4.format(SORUCE_EMJ, SORUCE_EMJ, Name_Channel, channel[0]))
    c_channel = redis.smembers(f"Must_Join {message.chat.id}")
    if channel[0] not in c_channel:
       redis.sadd(f"Must_Join {message.chat.id}", channel[0])
       return await eod(message, must_msg5.format(SORUCE_EMJ, Name_Channel, channel[0]))
    await eod(message, must_msg6.format(SORUCE_EMJ, Name_Channel, channel[0]))

@it_s6.on_message(filters.command(unmust_join_command, HNDLR) & filters.me)
async def unmust_join(client,message):
    from ..Helper import eod
    get_channel = message.text.split(f"{unmust_join_command} ")
    if len(get_channel) < 2:
        return await eod(message, must_msg1)
    channel = get_channel[1].split(" ")
    if channel[0].startswith("@"):
        return await eod(message, must_msg2)
    if channel[0].startswith("https://"):
        return await eod(message, must_msg2)
    try:
        Name_Channel = (await bot.get_chat(channel[0])).title
    except:
        pass
    c_channel = redis.smembers(f"Must_Join {message.chat.id}")
    if channel[0] in c_channel:
       redis.srem(f"Must_Join {message.chat.id}", channel[0])
       return await eod(message, must_msg7.format(SORUCE_EMJ, Name_Channel, channel[0]))
    await eod(message, must_msg8.format(SORUCE_EMJ, Name_Channel, channel[0]))

@bot.on_inline_query(filters.regex("^must_join_b$"))
async def must_join_b(client, inline_query):
      if len(channels_to_join) < 2:
       await inline_query.answer(
        results=[
            types.InlineQueryResultArticle(
                title="it_s6",
                input_message_content=types.InputTextMessageContent(msg1),
                reply_markup=types.InlineKeyboardMarkup(buttons_ch)
            ),
        ],
        cache_time=1
        )
      else:
        await inline_query.answer(
        results=[
            types.InlineQueryResultArticle(
                title="it_s6",
                input_message_content=types.InputTextMessageContent(msg2),
                reply_markup=types.InlineKeyboardMarkup(buttons_ch)
            ),
        ],
        cache_time=1
        )

async def must_join_ls(client, message):
    global channels_to_join, buttons_ch, msg1, msg2
    c_channel = redis.smembers(f"Must_Join {message.chat.id}")
    channels_to_join = []
    buttons_ch = []
    for channel_name in c_channel:
        try:
            await it_s6.get_chat_member(channel_name, message.from_user.id)
        except UserNotParticipant:
            channels_to_join.append(channel_name)
            Name_Channel = (await bot.get_chat(channel_name)).title
            buttons_ch.append ([types.InlineKeyboardButton(text=Name_Channel , url=f"https://t.me/{channel_name}")])
        except Exception:
            pass
    if channels_to_join:
        await message.delete()
        msg1 = must_msg9.format(SORUCE_EMJ, message.from_user.mention, SORUCE_EMJ)
        msg2 = must_msg10.format(SORUCE_EMJ, message.from_user.mention, SORUCE_EMJ)
        result = await it_s6.get_inline_bot_results(config.BOT_USER, query="must_join_b")
        await it_s6.send_inline_bot_result(message.chat.id, result.query_id, result.results[0].id)
    else:
        pass

back_button = types.InlineKeyboardMarkup(
            [[
             types.InlineKeyboardButton(b_button,callback_data="B_MJ"),
             ]]
             )

@bot.on_callback_query(filters.regex('^b_must_join'))
async def b_must_join(client, callback_query):
    if callback_query.from_user.id != it_s6.me.id:
       return await bot.answer_callback_query(callback_query.id, text=c_me, show_alert=True)
    return await callback_query.edit_message_text(
        strings.HELP_CMD.format(module=__mod_name__, help=__help__),
        reply_markup=back_button)

@bot.on_callback_query(filters.regex('^B_MJ'))
async def B_MJ(client, callback_query):
    if callback_query.from_user.id != it_s6.me.id:
       return await bot.answer_callback_query(callback_query.id, text=c_me, show_alert=True)
    return await callback_query.edit_message_text(
        text="", 
        reply_markup=MENU, 
        parse_mode=enums.ParseMode.MARKDOWN
    )

__mod_name__ = "Must Join"  
    
__help__ = f"""  

{SORUCE_EMJ} `{HNDLR}{must_join_command}`
{must_join_us}

{SORUCE_EMJ} `{HNDLR}{unmust_join_command}`
{unmust_join_us}

{My_User}
"""
    
string = {"module": __mod_name__, "help": __help__}   
MODULE.append(string)
