from pyrogram import filters, enums, types
from IT_S6 import it_s6, bot, redis, My_User, SORUCE_EMJ, HNDLR, MODULE
from pyrogram.errors import FloodWait
from .__Help import MENU
from ..Langs import *
import datetime, pytz, asyncio, config, strings

it_emj = redis.get("AUTO_EMOJI") or "|"
it_font1 = "0123456789"
it_font2 = redis.get("AUTO_FONT") or "𝟎𝟏𝟐𝟑𝟒𝟓𝟔𝟕𝟖𝟗"

async def auto_italia():
      while redis.exists("clock"):
            TimeZone_ITALIA = datetime.datetime.now(pytz.timezone(config.TZ))
            HM = TimeZone_ITALIA.strftime("%I:%M")
            for sa3ed in HM:
                if sa3ed in it_font1:
                   it_font = it_font2[it_font1 .index(sa3ed)]
                   HM = HM.replace(sa3ed, it_font)
            name = f"{HM} {it_emj}"
            try:
                await it_s6.update_profile(first_name = f"{name}")
            except FloodWait as e:
                await asyncio.sleep(e.value)
            await asyncio.sleep(60)

@it_s6.on_message(filters.command(autoname_command, HNDLR) & filters.me)
async def start_time(client, message):
    from ..Helper import eod
    m_name = message.from_user.first_name
    if not redis.exists("clock"):
        asyncio.ensure_future(auto_italia())
        redis.set("clock", m_name)
        await eod(message, auto_msg1)
    else:
        await eod(message, auto_msg2)

@it_s6.on_message(filters.command(sautoname_command, HNDLR) & filters.me)
async def stop_time(client, message):
    from ..Helper import eod
    if not redis.exists("clock"):
      await eod(message, auto_msg3)
    else:
      name = redis.get("clock")
      await it_s6.update_profile(first_name = f"{name}")
      redis.delete("clock")
      await eod(message, auto_msg4)

back_button = types.InlineKeyboardMarkup(
            [[
             types.InlineKeyboardButton(b_button,callback_data="B_A"),
             ]]
             )

@bot.on_callback_query(filters.regex('^b_autoname'))
async def b_mute(client, callback_query):
    if callback_query.from_user.id != it_s6.me.id:
       return await bot.answer_callback_query(callback_query.id, text=c_me, show_alert=True)
    return await callback_query.edit_message_text(
        strings.HELP_CMD.format(module=__mod_name__, help=__help__),
        reply_markup=back_button)

@bot.on_callback_query(filters.regex('^B_A'))
async def B_1(client, callback_query):
    if callback_query.from_user.id != it_s6.me.id:
       return await bot.answer_callback_query(callback_query.id, text=c_me, show_alert=True)
    return await callback_query.edit_message_text(
        text="", 
        reply_markup=MENU, 
        parse_mode=enums.ParseMode.MARKDOWN
    )

__mod_name__ = "Autoname"  
    
__help__ = f"""  

{SORUCE_EMJ} `{HNDLR}{autoname_command}`
{autoname_us}

{SORUCE_EMJ} `{HNDLR}{sautoname_command}`
{sautoname_us}

{My_User}
"""
    
    
string = {"module": __mod_name__, "help": __help__}   
MODULE.append(string)