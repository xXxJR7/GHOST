from IT_S6 import bot, it_s6, redis, SORUCE_EMJ
from pyrogram import filters, types
from telegraph import Telegraph, upload_file
from ..Langs import *
import os, sys, subprocess, asyncio

help_photo_url = "" or redis.get("Help_Pic")

telegraph = Telegraph()
r = telegraph.create_account(short_name="Sa3ed")
auth_url = r["auth_url"]

state = "normal"

SETTINGS = types.InlineKeyboardMarkup(
            [[
             types.InlineKeyboardButton(v,callback_data="settings"),
             types.InlineKeyboardButton(v7_,callback_data="v7"),
             ]
             ]
             )

VARS = types.InlineKeyboardMarkup(
            [[
             types.InlineKeyboardButton(v1_,callback_data="v1"),
             types.InlineKeyboardButton(v2_,callback_data="v2"),
             ],
             [
             types.InlineKeyboardButton(v3_,callback_data="v3"),
             types.InlineKeyboardButton(v4_,callback_data="v4"),
             ],
             [
             types.InlineKeyboardButton(v5_,callback_data="v5"),
             types.InlineKeyboardButton(v6_,callback_data="v6"),
             ],
             [
             types.InlineKeyboardButton(b_button,callback_data="S_ttings"),
             ]
             ])

R_LANGS = types.InlineKeyboardMarkup(
            [[
             types.InlineKeyboardButton(v_ar,callback_data="B_ar"),
             types.InlineKeyboardButton(v_en,callback_data="B_en"),
             ],
             [
             types.InlineKeyboardButton(b_button,callback_data="S_ttings"),
             ]
             ]
             )

R_PIC1 = types.InlineKeyboardMarkup(
            [[
             types.InlineKeyboardButton(v_rem,callback_data="r1_photo"),
             ],
             [
             types.InlineKeyboardButton(b_button,callback_data="VARS"),
             ]
             ]
             )

R_PIC2 = types.InlineKeyboardMarkup(
            [[
             types.InlineKeyboardButton(v_rem,callback_data="r2_photo"),
             ],
             [
             types.InlineKeyboardButton(b_button,callback_data="VARS"),
             ]
             ]
             )

R_HNDLR = types.InlineKeyboardMarkup(
            [[
             types.InlineKeyboardButton(v8_,callback_data="r1_hndlr"),
             ],
             [
             types.InlineKeyboardButton(b_button,callback_data="VARS"),
             ]
             ]
             )

auto_fonts = types.InlineKeyboardMarkup(
            [[
             types.InlineKeyboardButton("𝟭𝟮:𝟬𝟬",callback_data="a1"),
             types.InlineKeyboardButton("１２:００",callback_data="a2"),
             ],
             [
             types.InlineKeyboardButton("𝟏𝟐:𝟎𝟎",callback_data="a3"),
             types.InlineKeyboardButton("𝟙𝟚:𝟘𝟘",callback_data="a4"),
             ],
             [
             types.InlineKeyboardButton("₁₂:₀₀",callback_data="a5"),
             types.InlineKeyboardButton("١٢:٠٠",callback_data="a6"),
             ],
             [
             types.InlineKeyboardButton(b_button,callback_data="VARS"),
             ]
             ])

BACK = types.InlineKeyboardMarkup(
            [[
             types.InlineKeyboardButton(b_button,callback_data="VARS"),
             ]]
             )

BACK1 = types.InlineKeyboardMarkup(
            [[
             types.InlineKeyboardButton(b_button,callback_data="B_lang"),
             ]]
             )

@bot.on_message(filters.command("start") & filters.private)
async def admins(client, message):
    await message.delete()
    name = message.from_user.first_name
    if message.from_user.id != it_s6.me.id:
       await bot.send_message(message.chat.id, c_user2.format(SORUCE_EMJ, name, it_s6.me.first_name))
    else:
       await bot.send_message(message.chat.id, c_dev3, reply_markup=SETTINGS)

@bot.on_callback_query(filters.regex('^v1'))
async def v1(client, callback_query):
       global state
       if state == "normal":
          state = "awaiting_hndlr"
          await callback_query.edit_message_text(v_msg1, reply_markup=R_HNDLR)
       else:
          return
@bot.on_callback_query(filters.regex('^v2'))
async def v2(client, callback_query):
       global state, m
       if state == "normal":
          state = "awaiting_pm_pic"
          m = await callback_query.edit_message_text(v_msg2, reply_markup=R_PIC1)
       else:
          return
@bot.on_callback_query(filters.regex('^v3'))
async def v3(client, callback_query):
       global state, m
       if state == "normal":
          state = "awaiting_help_pic"
          m = await callback_query.edit_message_text(v_msg3, reply_markup=R_PIC2)
       else:
          return
@bot.on_callback_query(filters.regex('^v4'))
async def v4(client, callback_query):
       global state
       if state == "normal":
          state = "awaiting_emoji"
          await callback_query.edit_message_text(v_msg4, reply_markup=BACK)
       else:
          return
@bot.on_callback_query(filters.regex('^v5'))
async def v5(client, callback_query):
          await callback_query.edit_message_text(v_msg5, reply_markup=auto_fonts)
@bot.on_callback_query(filters.regex('^v6'))
async def v6(client, callback_query):
       global state
       if state == "normal":
          state = "awaiting_autoemoji"
          await callback_query.edit_message_text(v_msg6, reply_markup=BACK)
       else:
          return
@bot.on_callback_query(filters.regex('^a1'))
async def a1(client, callback_query):
        redis.set("AUTO_FONT", "𝟬𝟭𝟮𝟯𝟰𝟱𝟲𝟳𝟴𝟵")
        await callback_query.edit_message_text(v_msg7, reply_markup=BACK)
        await asyncio.sleep(0.5)
        subprocess.Popen([sys.executable, "-B", "-m", "IT_S6"], close_fds=True)
        sys.exit(0)
@bot.on_callback_query(filters.regex('^a2'))
async def a2(client, callback_query):
        redis.set("AUTO_FONT", "０１２３４５６７８９")
        await callback_query.edit_message_text(v_msg8, reply_markup=BACK)
        await asyncio.sleep(0.5)
        subprocess.Popen([sys.executable, "-B", "-m", "IT_S6"], close_fds=True)
        sys.exit(0)
@bot.on_callback_query(filters.regex('^a3'))
async def a3(client, callback_query):
        redis.set("AUTO_FONT", "𝟎𝟏𝟐𝟑𝟒𝟓𝟔𝟕𝟖𝟗")
        await callback_query.edit_message_text(v_msg9, reply_markup=BACK)
        await asyncio.sleep(0.5)
        subprocess.Popen([sys.executable, "-B", "-m", "IT_S6"], close_fds=True)
        sys.exit(0)
@bot.on_callback_query(filters.regex('^a4'))
async def a4(client, callback_query):
        redis.set("AUTO_FONT", "𝟘𝟙𝟚𝟛𝟜𝟝𝟞𝟟𝟠𝟡")
        await callback_query.edit_message_text(v_msg10, reply_markup=BACK)
        await asyncio.sleep(0.5)
        subprocess.Popen([sys.executable, "-B", "-m", "IT_S6"], close_fds=True)
        sys.exit(0)
@bot.on_callback_query(filters.regex('^a5'))
async def a5(client, callback_query):
        redis.set("AUTO_FONT", "₀₁₂₃₄₅₆₇₈₉")
        await callback_query.edit_message_text(v_msg11, reply_markup=BACK)
        await asyncio.sleep(0.5)
        subprocess.Popen([sys.executable, "-B", "-m", "IT_S6"], close_fds=True)
        sys.exit(0)
@bot.on_callback_query(filters.regex('^a6'))
async def a6(client, callback_query):
        redis.set("AUTO_FONT", "٠١٢٣٤٥٦٧٨٩")
        await callback_query.edit_message_text(v_msg12, reply_markup=BACK)
        await asyncio.sleep(0.5)
        subprocess.Popen([sys.executable, "-B", "-m", "IT_S6"], close_fds=True)
        sys.exit(0)
@bot.on_callback_query(filters.regex('^r1_photo'))
async def r1_photo(client, callback_query):
        if not redis.exists("PM_PIC"):
           return await callback_query.edit_message_text(v_msg13, reply_markup=BACK)
        redis.delete("PM_PIC")
        await callback_query.edit_message_text(v_msg14, reply_markup=BACK)
        await asyncio.sleep(0.5)
        subprocess.Popen([sys.executable, "-B", "-m", "IT_S6"], close_fds=True)
        sys.exit(0)
@bot.on_callback_query(filters.regex('^r2_photo'))
async def r2_photo(client, callback_query):
        if not redis.exists("Help_Pic"):
           return await callback_query.edit_message_text(v_msg15, reply_markup=BACK)
        redis.delete("Help_Pic")
        await callback_query.edit_message_text(v_msg16, reply_markup=BACK)
        await asyncio.sleep(0.5)
        subprocess.Popen([sys.executable, "-B", "-m", "IT_S6"], close_fds=True)
        sys.exit(0)
        
@bot.on_callback_query(filters.regex('^settings'))
async def settings(client, callback_query):
       global state
       state = "normal"
       await callback_query.edit_message_text(c_dev3, reply_markup=VARS)

@bot.on_callback_query(filters.regex('^VARS'))
async def VARSS(client, callback_query):
       global state
       state = "normal"
       await callback_query.edit_message_text(c_dev3, reply_markup=VARS)

@bot.on_callback_query(filters.regex('^S_ttings'))
async def S_ttings(client, callback_query):
       await callback_query.edit_message_text(c_dev3, reply_markup=SETTINGS)

@bot.on_callback_query(filters.regex('^B_lang'))
async def B_lang(client, callback_query):
       await callback_query.edit_message_text(c_dev3, reply_markup=R_LANGS)

@bot.on_callback_query(filters.regex('^v7'))
async def v7(client, callback_query):
          await callback_query.edit_message_text(v_msg17, reply_markup=R_LANGS)

@bot.on_callback_query(filters.regex('^r1_hndlr'))
async def r1_hndlr(client, callback_query):
          if "NO_HNDLR" in redis.get("HNDLR"):
             return await callback_query.edit_message_text(v_msg21__, reply_markup=BACK)
          redis.set("HNDLR", "NO_HNDLR")
          await callback_query.edit_message_text(v_msg21_, reply_markup=BACK)
          await asyncio.sleep(0.5)
          subprocess.Popen([sys.executable, "-B", "-m", "IT_S6"], close_fds=True)
          sys.exit(0)

@bot.on_callback_query(filters.regex('^B_ar'))
async def B_ar(client, callback_query):
        exists = redis.exists("LANGUAGE")
        if exists:
           languages = redis.smembers("LANGUAGE")
        else:
           languages = set()
        if "ar" in languages:
             return await callback_query.edit_message_text(v_msg18_, reply_markup=BACK1)
        redis.set("LANGUAGE", "ar")
        await callback_query.edit_message_text(v_msg18, reply_markup=BACK1)
        await asyncio.sleep(0.5)
        subprocess.Popen([sys.executable, "-B", "-m", "IT_S6"], close_fds=True)
        sys.exit(0)
        
@bot.on_callback_query(filters.regex('^B_en'))
async def B_en(client, callback_query):
        exists = redis.exists("LANGUAGE")
        if exists:
           languages = redis.smembers("LANGUAGE")
        else:
           languages = set()
        if "en" in languages:
             return await callback_query.edit_message_text(v_msg19_, reply_markup=BACK1)
        redis.set("LANGUAGE", "en")
        await callback_query.edit_message_text(v_msg19, reply_markup=BACK1)
        await asyncio.sleep(0.5)
        subprocess.Popen([sys.executable, "-B", "-m", "IT_S6"], close_fds=True)
        sys.exit(0)

@bot.on_message(filters.private & filters.user(it_s6.me.id))
async def cmd(client, message):
    global state
    if state in state_handlers:
       await state_handlers[state](client, message)

async def handle_emoji(client, message):
    help_emoji = message.text
    redis.set("SORUCE_EMJ", help_emoji)
    await message.reply(v_msg20.format(SORUCE_EMJ, help_emoji))
    await asyncio.sleep(0.5)
    subprocess.Popen([sys.executable, "-B", "-m", "IT_S6"], close_fds=True)
    sys.exit(0)

async def handle_hndlr(client, message):
    command_hndlr = message.text
    redis.set("HNDLR", command_hndlr)
    await message.reply(v_msg21.format(SORUCE_EMJ, command_hndlr))
    await asyncio.sleep(0.5)
    subprocess.Popen([sys.executable, "-B", "-m", "IT_S6"], close_fds=True)
    sys.exit(0)

async def handle_help_pic(client, message):
    c_photo = message.photo
    if not c_photo:
       return await message.reply(v_msg22)
    else:
        photo_path = "./sa3ed.jpg" 
        await message.download(photo_path)
        try:
            pic_url = f"https://graph.org{upload_file(photo_path)[0]}"
            redis.set("Help_Pic", pic_url)
            await message.delete()
            await m.delete()
            await message.reply_photo(photo_path, caption=v_msg23)
            os.remove(photo_path)
            await asyncio.sleep(0.5)
            subprocess.Popen([sys.executable, "-B", "-m", "IT_S6"], close_fds=True)
            sys.exit(0)
        except Exception as e:
            state = "normal"
            await message.reply(v_msg24)

async def handle_pm_pic(client, message):
    if message.photo:
       photo_path = "./sa3ed.jpg"
       await message.download(photo_path)
       pic_url = f"https://graph.org{upload_file(photo_path)[0]}"
       redis.set("PM_PIC", pic_url)
       await message.delete()
       await m.delete()
       await message.reply_photo(photo_path, caption=v_msg25)
       os.remove(photo_path)
    elif message.video:
       video_path = "./sa3ed.mp4"
       video_pic = "./sa3ed.jpg"
       await message.download(video_path)
       await message.download(video_pic)
       pic_url = f"https://graph.org{upload_file(video_path)[0]}"
       pic_url1 = f"https://graph.org{upload_file(video_pic)[0]}"
       redis.set("PM_PIC", pic_url)
       redis.set("PM_PIC1", pic_url1)
       await message.delete()
       await m.delete()
       await message.reply_video(video_path, caption=v_msg25)
       os.remove(video_path)
       os.remove(video_pic)
    else:
       await message.reply(v_msg26)
    await asyncio.sleep(0.5)
    subprocess.Popen([sys.executable, "-B", "-m", "IT_S6"], close_fds=True)
    sys.exit(0)

async def handle_autoemoji(client, message):
    auto_emoji = message.text
    redis.set("AUTO_EMOJI", auto_emoji)
    await message.reply(v_msg27.format(SORUCE_EMJ, auto_emoji))
    await asyncio.sleep(0.5)
    subprocess.Popen([sys.executable, "-B", "-m", "IT_S6"], close_fds=True)
    sys.exit(0)

state_handlers = {"awaiting_emoji": handle_emoji,
                  "awaiting_hndlr": handle_hndlr,
                  "awaiting_help_pic": handle_help_pic,
                  "awaiting_pm_pic": handle_pm_pic,
                  "awaiting_autoemoji":handle_autoemoji}
