from IT_S6 import it_s6, redis
from pyrogram import filters
from .Mute import listen_gr2, listen_gr1
from .Must_Join import must_join_ls
from .prevent import Forbidden_Words_ls, preventuserbot_ls

@it_s6.on_message(filters.group & filters.create(lambda it, s6, message: redis.get("s_log") is not None and "True" in redis.get("s_log")) & ~filters.me)
async def forward_func(client, message):
  user = await it_s6.get_messages(message.chat.id, message.id)
  chat = str(user.chat.id)
  ids = chat.replace("-100","")
  message_id = user.id
  reply_user = types.InlineKeyboardMarkup([[
                types.InlineKeyboardButton(f"{user.chat.title}",url=f"https://t.me/c/={ids}/={message_id}")
                ],
                [
                types.InlineKeyboardButton(f"{user.from_user.first_name}",url=f"https://t.me/{user.from_user.username}")
                ]])
  reply_none_user = types.InlineKeyboardMarkup([[
                types.InlineKeyboardButton(f"{user.chat.title}",url=f"https://t.me/c/={ids}/={message_id}")
                ],
                [
                types.InlineKeyboardButton(f"{user.from_user.first_name}",url=f"https://t.me/c/={ids}/={message_id}")
                ]])
  try:
     g = await it_s6.get_chat_member(message.chat.id, message.from_user.id)
  except:
     pass
  if message.mentioned:
    if not g.user.is_bot:
         if message.photo:
            s1 = await message.download()
            if message.caption:
               await bot.send_photo(int(LOG), photo =s1, caption = f"{message.caption}", reply_markup=reply_user)
               os.remove(s1)
               return
            else:
               await bot.send_photo(int(LOG), photo =s1, reply_markup=reply_user)
               os.remove(s1)
               return
         if message.sticker:
            if user.from_user.username is None:
               return await bot.send_sticker(int(LOG), sticker =message.sticker.file_id, reply_markup=reply_none_user)
            await bot.send_sticker(int(LOG), sticker =message.sticker.file_id, reply_markup=reply_user)
         if message.voice:
            s2 = await message.download()
            if user.from_user.username is None:
               await bot.send_audio(int(LOG), audio = s2, reply_markup=reply_none_user)
               os.remove(s2)
               return
            else:
               await bot.send_audio(int(LOG), audio = s2, reply_markup=reply_user)
               os.remove(s2)
               return
         if message.animation:
            s3 = await message.download()
            if user.from_user.username is None:
               await bot.send_animation(int(LOG), animation = s3, reply_markup=reply_none_user)
               os.remove(s3)
               return
            else:
               await bot.send_animation(int(LOG), animation = s3, reply_markup=reply_user)
               os.remove(s3)
               return
         if message.text:
            if user.from_user.username is None:
               return await bot.send_message(int(LOG),f"{user.text}",reply_markup=reply_none_user)
            await bot.send_message(int(LOG),f"{user.text}",reply_markup=reply_user)

@it_s6.on_message(filters.group & ~filters.me & ~filters.bot)
async def on_message(client, message):
    if message.from_user:
        if str(message.chat.id) in redis.smembers("mute_all"):
            await listen_gr2(client, message)
        if str(message.from_user.id) in redis.smembers(f"mute_in_chat:{message.chat.id}"):
            await listen_gr1(client, message)
        elif redis.smembers(f"must_join {message.chat.id}"):
            await must_join_ls(client, message)
        if redis.smembers(f"Forbidden_Words {message.chat.id}"):
            await Forbidden_Words_ls(client, message)
        if str(message.chat.id) in redis.smembers("Prevent_Userbot"):
            await preventuserbot_ls(client, message)
