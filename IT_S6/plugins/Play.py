import config, strings, os, datetime, shutil
from IT_S6 import it_s6, bot, app, it_s6_music, redis, My_User, HNDLR, SORUCE_EMJ, MODULE
from ..Langs import *
from .__Help import R_MENU
from pytube import YouTube
from youtubesearchpython import SearchVideos
from yt_dlp import YoutubeDL
from pyrogram import filters, types, enums
from pytgcalls.types.input_stream import AudioVideoPiped
from pytgcalls.types import AudioPiped, Update
from pytgcalls.types.input_stream.quality import HighQualityAudio, HighQualityVideo

active = []
stream = {}

async def is_active_chat(chat_id: int) -> bool:
    if chat_id not in active:
        return False
    else:
        return True

async def add_active_chat(chat_id: int):
    if chat_id not in active:
        active.append(chat_id)

async def remove_active_chat(chat_id: int):
    if chat_id in active:
        active.remove(chat_id)

async def is_streaming(chat_id: int) -> bool:
    run = stream.get(chat_id)
    if not run:
        return False
    return run

async def stream_on(chat_id: int):
    stream[chat_id] = True

def m_menu(chat_id):
    PAUSE_markup = types.InlineKeyboardMarkup(
            [[
             types.InlineKeyboardButton("𝐒𝐓𝐎𝐏",callback_data=f"IT_STOP_{chat_id}"),
             types.InlineKeyboardButton("𝐏𝐀𝐔𝐒𝐄",callback_data=f"IT_PAUSE_{chat_id}"),
             types.InlineKeyboardButton("𝐒𝐊𝐈𝐏",callback_data=f"IT_SKIP_{chat_id}"),
            ]
             ])
    return PAUSE_markup

def m2_menu(chat_id):
    REUSME_markup = types.InlineKeyboardMarkup(
            [[
             types.InlineKeyboardButton("𝐑𝐄𝐔𝐒𝐌𝐄",callback_data=f"IT_REUSME_{chat_id}"),
             ]
             ])
    return REUSME_markup

@bot.on_callback_query(filters.regex(r"IT_PAUSE_"))
async def it_pause(client, callback_query):
    chat_id = int(callback_query.data.split("_")[2])
    await app.pause_stream(chat_id)
    await callback_query.edit_message_text(msg+pp,reply_markup=m2)

@bot.on_callback_query(filters.regex(r"IT_REUSME_"))
async def it_resume(client, callback_query):
    chat_id = int(callback_query.data.split("_")[2])
    await app.resume_stream(chat_id)
    await callback_query.edit_message_text(msg+pr,reply_markup=m1)

@bot.on_callback_query(filters.regex(r"IT_STOP_"))
async def it_pause(client, callback_query):
    from ..Helper import sod
    chat_id = int(callback_query.data.split("_")[2])
    last_music_msg_ids = redis.hget('last_music_msg_ids', chat_id)
    await _clear_(chat_id)
    await app.leave_group_call(chat_id)
    await it_s6.delete_messages(chat_id, int(last_music_msg_ids))
    await sod(chat_id, pe)

@bot.on_callback_query(filters.regex(r"IT_SKIP_"))
async def it_skip(client, callback_query):
    from ..Helper import sod
    global msg
    chat_id = int(callback_query.data.split("_")[2])
    last_music_msg_ids = redis.hget('last_music_msg_ids', chat_id)
    get = it_s6_lis.get(chat_id)
    try:
        await it_s6.delete_messages(chat_id, int(last_music_msg_ids))
    except :
        print(f"Failed to delete previous warning message")
    if not get:
        try:
            await _clear_(chat_id)
            await app.leave_group_call(chat_id)
            await sod(chat_id, ps)
        except:
            return
    else:
        title = get[0]["title"]
        duration = get[0]["duration"]
        file_path = get[0]["file_path"]
        get.pop(0)
        result = await it_s6.get_inline_bot_results(config.BOT_USER, query="music")
        s6 = await it_s6.send_inline_bot_result(chat_id, result.query_id, result.results[0].id)
        message_id = s6.updates[0].id
        redis.hset('last_music_msg_ids', chat_id, message_id)
        msg = p1.format(SORUCE_EMJ, title, SORUCE_EMJ, duration)
        if file_path.endswith("mp4") or file_path.endswith("MOV"):
            try:
               await app.change_stream(
                chat_id,
                AudioVideoPiped(
                    file_path,
                    HighQualityAudio(),
                    HighQualityVideo(),
                )
            )
            except:
               await _clear_(chat_id)
               return await app.leave_group_call(chat_id)
        else:
            try:
               await app.change_stream(
                chat_id,
                AudioPiped(
                    file_path,
                    HighQualityAudio(),
                )
            )
            except:
               await _clear_(chat_id)
               return await app.leave_group_call(chat_id)

@bot.on_inline_query(filters.regex("^music$"))
async def music_inl(client, inline_query):
       await inline_query.answer(
        results=[
            types.InlineQueryResultArticle(
                title="it_s6",
                input_message_content=types.InputTextMessageContent(msg),
                reply_markup=m1
            ),
        ],
        cache_time=1
        )

it_s6_lis = {}

async def put(
    chat_id,
    title,
    duration,
    file_path,
):
    put_f = {
        "title": title,
        "duration": duration,
        "file_path": file_path,
    }
    get = it_s6_lis.get(chat_id)
    if get:
        it_s6_lis[chat_id].append(put_f)
    else:
        it_s6_lis[chat_id] = []
        it_s6_lis[chat_id].append(put_f)

@it_s6.on_message(filters.command(add_command, HNDLR) & filters.me & filters.group)
async def addd_command(client, message):
    from ..Helper import eod
    rep = message.reply_to_message
    if not rep:
       return await eod(message, c_user)
    exists = redis.exists("SUDOERS")
    if exists:
        sudoers = redis.smembers("SUDOERS")
    else:
        sudoers = set()
    if str(rep.from_user.id) in sudoers:
       return await eod(message, add1.format(SORUCE_EMJ, rep.from_user.mention))
    redis.sadd("SUDOERS", rep.from_user.id)
    await eod(message, add2.format(SORUCE_EMJ, rep.from_user.mention))

@it_s6.on_message(filters.command(del_command, HNDLR) & filters.me & filters.group)
async def dell_command(client, message):
    from ..Helper import eod
    rep = message.reply_to_message
    if not rep:
       return await eod(message, c_user)
    exists = redis.exists("SUDOERS")
    if exists:
        sudoers = redis.smembers("SUDOERS")
    else:
        sudoers = set()
    if str(rep.from_user.id) not in sudoers:
       return await eod(message, rem1.format(SORUCE_EMJ, rep.from_user.mention))
    redis.srem("SUDOERS", rep.from_user.id)
    await eod(message, rem2.format(SORUCE_EMJ, rep.from_user.mention))

from pyrogram.raw.functions.phone import CreateGroupCall as g
@it_s6.on_message(filters.command(play_command, HNDLR) & filters.group)
async def playa_command(client, message):
    from ..Helper import sod
    global m1, m2, msg
    try:
        await message.delete()
    except:
        pass
    exists = redis.exists("SUDOERS")
    if exists:
        sudoers = redis.smembers("SUDOERS")
    else:
        sudoers = set()
    if str(message.from_user.id) in sudoers:
        m1 = m_menu(message.chat.id)
        m2 = m2_menu(message.chat.id)
        text = message.text.split(None, 1)
        if not len(text) > 1:
            await message.delete()
            return await sod(message.chat.id, c_command)
        text = text[1]
        await message.delete()
        msg1 = await message.reply(search_m)
        try:
            Sa3ed = await it_s6.create_chat_invite_link(message.chat.id)
            await it_s6_music.join_chat(Sa3ed.invite_link)
        except:
            pass
        try:
            input_peer = await it_s6.resolve_peer(message.chat.id)
            await it_s6.invoke(g(peer=input_peer, random_id=26))
        except:
            pass
        search = SearchVideos(text, offset=1, mode="dict", max_results=1)
        mi = search.result()
        mio = mi["search_result"]
        mo = mio[0]["link"]
        mio[0]["duration"]
        mio[0]["channel"]
        output_path = "/Test"
        opts = {
            'format': 'bestaudio/best',
            'keepvideo': False,
            'prefer_ffmpeg': True,
            'geo_bypass': True,
            'outtmpl': os.path.join(output_path, '%(title)s.%(ext)s'),
            'quite': True,
        }
        try:
            with YoutubeDL(opts) as ytdl:
                ytdl_data = ytdl.extract_info(mo, download=True)
                audio_file = ytdl.prepare_filename(ytdl_data)
        except:
            return await msg1.edit(d_failed)
        duration = ytdl_data['duration']
        duration_hms = str(datetime.timedelta(seconds=int(duration)))
        msg = p1.format(SORUCE_EMJ, ytdl_data['title'], SORUCE_EMJ, duration_hms)
        last_music_msg_ids = redis.hget('last_music_msg_ids', message.chat.id)
        if await is_active_chat(message.chat.id):
           await msg1.delete()
           await put(
                    message.chat.id,
                    ytdl_data['title'],
                    duration_hms,
                    audio_file
                )
           position = len(it_s6_lis.get(message.chat.id))
           await message.reply(p2.format(SORUCE_EMJ, position, SORUCE_EMJ, ytdl_data['title'], SORUCE_EMJ, duration_hms))
        else:
          try:
            await msg1.delete()
            await app.join_group_call(
                message.chat.id,
                AudioPiped(
                    audio_file,
                    HighQualityAudio(),
                )
            )
            try:
                await it_s6.delete_messages(message.chat.id, int(last_music_msg_ids))
            except Exception as e:
                print(f"Failed to delete previous warning message: {e}")
            result = await it_s6.get_inline_bot_results(config.BOT_USER, query="music")
            s6 = await it_s6.send_inline_bot_result(message.chat.id, result.query_id, result.results[0].id)
            message_id = s6.updates[0].id
            redis.hset('last_music_msg_ids', message.chat.id, message_id)
            await stream_on(message.chat.id)
            await add_active_chat(message.chat.id)
          except:
            await sod(message.chat.id, p_err)

async def progress(current, total):
    print(f"{current * 100 / total:.1f}%")

@it_s6.on_message(filters.command(video_command, HNDLR) & filters.group)
async def playv_command(client, message):
    from ..Helper import sod
    global m1, m2, photo, msg
    try:
        await message.delete()
    except:
        pass
    exists = redis.exists("SUDOERS")
    if exists:
        sudoers = redis.smembers("SUDOERS")
    else:
        sudoers = set()
    if str(message.from_user.id) in sudoers:
      m1 = m_menu(message.chat.id)
      m2 = m2_menu(message.chat.id)
      text = message.text.split(None, 1)
      if not len(text) > 1:
            rep = message.reply_to_message
            
            if not rep or not rep.video and not rep.document:
               return await sod(message.chat.id, c_command)
            try:
                Sa3ed = await it_s6.create_chat_invite_link(message.chat.id)
                await it_s6_music.join_chat(Sa3ed.invite_link)
            except:
                pass
            try:
                input_peer = await it_s6.resolve_peer(message.chat.id)
                await it_s6.invoke(g(peer=input_peer, random_id=26))
            except:
                pass
            media = (rep.video or rep.document)
            duration_hms = str(datetime.timedelta(seconds=int(media.duration)))
            msg2 = await message.reply(d1)
            path =await it_s6.download_media(media, progress=progress)
            ms1 = await msg2.edit(d2)
            msg = p1.format(SORUCE_EMJ, media.file_name, SORUCE_EMJ, duration_hms)
            if await is_active_chat(message.chat.id):
               await ms1.delete()
               await put(
                    message.chat.id,
                    media.file_name,
                    duration_hms,
                    path
                )
               position = len(it_s6_lis.get(message.chat.id))
               
               await message.reply(p2.format(SORUCE_EMJ, position, SORUCE_EMJ, media.file_name, SORUCE_EMJ, duration_hms))
            else:
               await ms1.delete()
               await app.join_group_call(
                message.chat.id,
                AudioVideoPiped(
                    path,
                    HighQualityAudio(),
                    HighQualityVideo(),
                )
            )
               try:
                 await it_s6.delete_messages(message.chat.id, int(last_music_msg_ids))
               except Exception as e:
                 print(f"Failed to delete previous warning message: {e}")
               result = await it_s6.get_inline_bot_results(config.BOT_USER, query="music")
               s6 = await it_s6.send_inline_bot_result(message.chat.id, result.query_id, result.results[0].id)
               message_id = s6.updates[0].id
               redis.hset('last_music_msg_ids', message.chat.id, message_id)
               await stream_on(message.chat.id)
               await add_active_chat(message.chat.id)
      else:
       text = text[1]
       if "youtu.be" in text:
        m = await message.reply(d1)
        yt = YouTube(text)
        video = yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first()
        video_path = video.download("./Test")
        duration_hms = str(datetime.timedelta(seconds=int(yt.length)))
        msg = p1.format(SORUCE_EMJ, yt.title, SORUCE_EMJ, duration_hms)
        if await is_active_chat(message.chat.id):
           await m.delete()
           await put(
                    message.chat.id,
                    yt.title,
                    duration_hms,
                    video_path
                )
           position = len(it_s6_lis.get(message.chat.id))
           await message.reply(p2.format(SORUCE_EMJ, position, SORUCE_EMJ, yt.title, SORUCE_EMJ, duration_hms))
        else:
          try:
            await m.delete()
            await app.join_group_call(
                message.chat.id,
                AudioVideoPiped(
                    video_path,
                    HighQualityAudio(),
                    HighQualityVideo(),
                )
            )
            try:
                await it_s6.delete_messages(message.chat.id, int(last_music_msg_ids))
            except Exception as e:
                print(f"Failed to delete previous warning message: {e}")
            result = await it_s6.get_inline_bot_results(config.BOT_USER, query="music")
            s6 = await it_s6.send_inline_bot_result(message.chat.id, result.query_id, result.results[0].id)
            message_id = s6.updates[0].id
            redis.hset('last_music_msg_ids', message.chat.id, message_id)
            await stream_on(message.chat.id)
            await add_active_chat(message.chat.id)
          except Exception:
            await sod(message.chat.id, p_err)
       else:
        msg1 = await message.reply(search_m)
        try:
            Sa3ed = await it_s6.create_chat_invite_link(message.chat.id)
            await it_s6_music.join_chat(Sa3ed.invite_link)
        except:
            pass
        try:
            input_peer = await it_s6.resolve_peer(message.chat.id)
            await it_s6.invoke(g(peer=input_peer, random_id=26))
        except:
            pass
        search = SearchVideos(text, offset=1, mode="dict", max_results=1)
        mi = search.result()
        mio = mi["search_result"]
        mo = mio[0]["link"]
        mio[0]["duration"]
        mio[0]["channel"]
        output_path = "/Test"
        opts = {
            'format': 'best',
            'keepvideo': True,
            'prefer_ffmpeg': True,
            'geo_bypass': True,
            'outtmpl': os.path.join(output_path, '%(title)s.%(ext)s'),
            'quite': True,
        }
        try:
            with YoutubeDL(opts) as ytdl:
                ytdl_data = ytdl.extract_info(mo, download=True)
                audio_file = ytdl.prepare_filename(ytdl_data)
        except :
            return await msg1.edit(d_failed)
        duration = ytdl_data['duration']
        duration_hms = str(datetime.timedelta(seconds=int(duration)))
        msg = p1.format(SORUCE_EMJ, ytdl_data['title'], SORUCE_EMJ, duration_hms)
        last_music_msg_ids = redis.hget('last_music_msg_ids', message.chat.id)
        if await is_active_chat(message.chat.id):
           await msg1.delete()
           await put(
                    message.chat.id,
                    ytdl_data['title'],
                    duration_hms,
                    audio_file
                )
           position = len(it_s6_lis.get(message.chat.id))
           await message.reply(p2.format(SORUCE_EMJ, position, SORUCE_EMJ, ytdl_data['title'], SORUCE_EMJ, duration_hms))
        else:
          try:
            await msg1.delete()
            await app.join_group_call(
                message.chat.id,
                AudioVideoPiped(
                    audio_file,
                    HighQualityAudio(),
                    HighQualityVideo(),
                )
            )
            try:
                await it_s6.delete_messages(message.chat.id, int(last_music_msg_ids))
            except Exception as e:
                print(f"Failed to delete previous warning message: {e}")
            result = await it_s6.get_inline_bot_results(config.BOT_USER, query="music")
            s6 = await it_s6.send_inline_bot_result(message.chat.id, result.query_id, result.results[0].id)
            message_id = s6.updates[0].id
            redis.hset('last_music_msg_ids', message.chat.id, message_id)
            await stream_on(message.chat.id)
            await add_active_chat(message.chat.id)
          except Exception:
            await sod(message.chat.id, p_err)

async def _clear_(chat_id):
    try:
        it_s6_lis[chat_id] = []
        await remove_active_chat(chat_id)
    except:
        return

@app.on_stream_end()
async def on_stream_end(client, update: Update):
    global msg
    chat_id = update.chat_id
    get = it_s6_lis.get(chat_id)
    if not get:
        try:
            await _clear_(chat_id)
            return await app.leave_group_call(chat_id)
        except:
            return
    else:
        title = get[0]["title"]
        duration = get[0]["duration"]
        file_path = get[0]["file_path"]
        get.pop(0)
        if file_path.endswith("mp4") or file_path.endswith("MOV"):
            try:
               await app.change_stream(
                chat_id,
                AudioVideoPiped(
                    file_path,
                    HighQualityAudio(),
                    HighQualityVideo(),
                )
            )
            except:
               await _clear_(chat_id)
               return await app.leave_group_call(chat_id)
        else:
            try:
               await app.change_stream(
                chat_id,
                AudioPiped(
                    file_path,
                    HighQualityAudio(),
                )
            )
            except:
               await _clear_(chat_id)
               return await app.leave_group_call(chat_id)
        msg = p1.format(SORUCE_EMJ, title, SORUCE_EMJ, duration)
        last_music_msg_ids = redis.hget('last_music_msg_ids', chat_id)
        try:
            await it_s6.delete_messages(chat_id, int(last_music_msg_ids))
        except Exception as e:
            print(f"Failed to delete previous warning message: {e}")
        result = await it_s6.get_inline_bot_results(config.BOT_USER, query="music")
        s6 = await it_s6.send_inline_bot_result(chat_id, result.query_id, result.results[0].id)
        message_id = s6.updates[0].id
        redis.hset('last_music_msg_ids', chat_id, message_id)

from apscheduler.schedulers.asyncio import AsyncIOScheduler
sa3ed = AsyncIOScheduler()

async def delete_files():
    try:
       shutil.rmtree('downloads')
    except:
       try:
          shutil.rmtree('Test')
       except:
          pass

sa3ed.add_job(delete_files, trigger="cron", hour=10, minute=0)
sa3ed.start()

back_button = types.InlineKeyboardMarkup(
            [[
             types.InlineKeyboardButton(b_button,callback_data="B_pla"),
             ]]
             )

@bot.on_callback_query(filters.regex('^b_play'))
async def b_play(client, callback_query):
    if callback_query.from_user.id != it_s6.me.id:
       return await bot.answer_callback_query(callback_query.id, text=c_me, show_alert=True)
    return await callback_query.edit_message_text(
        strings.HELP_CMD.format(module=__mod_name__, help=__help__),
        reply_markup=back_button)

@bot.on_callback_query(filters.regex('^B_pla'))
async def B_pla(client, callback_query):
    if callback_query.from_user.id != it_s6.me.id:
       return await bot.answer_callback_query(callback_query.id, text=c_me, show_alert=True)
    return await callback_query.edit_message_text(
        text="", 
        reply_markup=R_MENU, 
        parse_mode=enums.ParseMode.MARKDOWN
    )

__mod_name__ = "Play"  
    
__help__ = f"""  

{SORUCE_EMJ} `{HNDLR}{play_command}`
{play_command_us}

{SORUCE_EMJ} `{HNDLR}{video_command}`
{video_command_us}

{SORUCE_EMJ} `{HNDLR}{add_command}`
{add_command_us}

{SORUCE_EMJ} `{HNDLR}{del_command}`
{del_command_us}

{My_User}
"""
    
    
string = {"module": __mod_name__, "help": __help__}   
MODULE.append(string)
