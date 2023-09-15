from IT_S6 import it_s6, bot, redis, My_User, SORUCE_EMJ, HNDLR, MODULE
from pyrogram import filters, enums, types
from pyrogram.errors import UserNotParticipant
from .__Help import MENU
from ..Langs import *
import strings

@it_s6.on_message(filters.command(must_join_command, HNDLR) & filters.me)
async def must_join(client,message):
    from ..Helper import eod
    get_channel = message.text.split(f"{must_join_command} ")
    if len(get_channel) < 2:
        return await eod(message, must_msg1)
    channel = get_channel[1].split(" ")
    if not channel[0].startswith("@"):
        return await eod(message, must_msg2)
    try:
       c_me = await it_s6.get_chat_member(channel[0], it_s6.me.id)
    except:
       return await eod(message, must_msg3.format(SORUCE_EMJ, channel[0]))
    if c_me.status not in [enums.ChatMemberStatus.OWNER, enums.ChatMemberStatus.ADMINISTRATOR]:
       return await eod(message, must_msg4.format(SORUCE_EMJ, SORUCE_EMJ, channel[0]))
    c_channel = redis.smembers(f"must_join {message.chat.id}")
    if channel[0] not in c_channel:
       redis.sadd(f"must_join {message.chat.id}", channel[0])
       return await eod(message, must_msg5.format(SORUCE_EMJ, channel[0]))
    await eod(message, must_msg6.format(SORUCE_EMJ, channel[0]))

@it_s6.on_message(filters.command(unmust_join_command, HNDLR) & filters.me)
async def unmust_join(client,message):
    from ..Helper import eod
    get_channel = message.text.split(f"{unmust_join_command} ")
    if len(get_channel) < 2:
        return await eod(message, must_msg1)
    channel = get_channel[1].split(" ")
    if not channel[0].startswith("@"):
        return await eod(message, must_msg2)
    c_channel = redis.smembers(f"must_join {message.chat.id}")
    if channel[0] in c_channel:
       redis.srem(f"must_join {message.chat.id}", channel[0])
       return await eod(message, must_msg7.format(SORUCE_EMJ, channel[0]))
    await eod(message, must_msg8.format(SORUCE_EMJ, channel[0]))

async def must_join_ls(client, message):
    c_channel = redis.smembers(f"must_join {message.chat.id}")
    channels_to_join = []
    for channel_name in c_channel:
        try:
            await it_s6.get_chat_member(channel_name, message.from_user.id)
        except UserNotParticipant:
            pass
            channels_to_join.append(channel_name)
        except Exception:
            pass
    if channels_to_join:
        await message.delete()
        if len(channels_to_join) < 2:
           await message.reply(must_msg9.format(SORUCE_EMJ, message.from_user.mention, SORUCE_EMJ, SORUCE_EMJ, ' ,'.join(channels_to_join)))
        else:
           await message.reply(must_msg10.format(SORUCE_EMJ, message.from_user.mention, SORUCE_EMJ, SORUCE_EMJ, ' ,'.join(channels_to_join)))
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