from pyrogram import filters, enums, types
from IT_S6 import it_s6, bot, redis, My_User, HNDLR, SORUCE_EMJ, MODULE
from .__Help import R_MENU
from ..Langs import *
from os import remove
import os, strings

@it_s6.on_message(filters.command(clone_command, HNDLR) & filters.me)
async def clone_user(client, message):
    from ..Helper import eod
    my_info = await it_s6.get_chat(it_s6.me.id)
    if message.reply_to_message and message.reply_to_message.from_user:
      id = message.reply_to_message.from_user.id
    else:
      return await eod(message, c_user)
    e = await message.edit(clone_msg1)
    redis.set(f'{it_s6.me.id}:clone_first_name', my_info.first_name)
    if my_info.bio:
       redis.set(f'{it_s6.me.id}:clone_bio', my_info.bio)
    if my_info.last_name:
       redis.set(f'{it_s6.me.id}:clone_last_name', my_info.last_name)
    if my_info.username:
       redis.set(f'{it_s6.me.id}:clone_username', my_info.username)
    if my_info.photo:
        async for photo in it_s6.get_chat_photos("me"):
            await it_s6.download_media(photo.file_id)
    us_info = await it_s6.get_chat(id)
    await it_s6.update_profile(first_name=us_info.first_name)
    if us_info.bio:
       await it_s6.update_profile(bio=us_info.bio)
    else:
       await it_s6.update_profile(bio="")
    if us_info.last_name:
       await it_s6.update_profile(last_name=us_info.last_name)
    else:
       await it_s6.update_profile(last_name="")
    if us_info.username:
       try:
         await it_s6.set_username(us_info.username+"s6")
       except:
         pass
    else:
       await it_s6.set_username("")
    if us_info.photo:
       async for photos in it_s6.get_chat_photos(id):
          his_photo = photos.file_id
          await it_s6.download_media(his_photo,file_name="./clone_photo.jpg")
          if my_info.photo:
             photos = [p async for p in it_s6.get_chat_photos("me")]
             await it_s6.delete_profile_photos([p.file_id for p in photos[0:]])
             await it_s6.set_profile_photo(photo="./clone_photo.jpg")
          else:
             await it_s6.set_profile_photo(photo="./clone_photo.jpg")
          remove("./clone_photo.jpg")
          break
    else:
       redis.set(f'{it_s6.me.id}:clone_c_photo', "No Photo")
    await eod(message, clone_msg2)

@it_s6.on_message(filters.command(unclone_command, HNDLR) & filters.me)
async def unclone_user(client, message):
   from ..Helper import eod
   my_info = await it_s6.get_chat(it_s6.me.id)
   first_name = redis.get(f'{it_s6.me.id}:clone_first_name')
   last_name = redis.get(f'{it_s6.me.id}:clone_last_name')
   user_name = redis.get(f'{it_s6.me.id}:clone_username')
   bio = redis.get(f'{it_s6.me.id}:clone_bio')
   c_photo = redis.get(f'{it_s6.me.id}:clone_c_photo')
   if not redis.get(f'{it_s6.me.id}:clone_first_name'):
      return await eod(message, clone_err)
   if not os.path.exists("downloads"):
        os.makedirs("downloads")
   photo_files = [file for file in os.listdir("downloads") if file.endswith(".jpg")]
   await message.edit(clone_msg3)
   if first_name:
      await it_s6.update_profile(first_name=first_name)
   if last_name:
      await it_s6.update_profile(last_name=last_name)
   else:
      await it_s6.update_profile(last_name="")
   if user_name:
      try:
         await it_s6.set_username(user_name)
      except:
         pass
   else:
      try:
         await it_s6.set_username("")
      except:
         pass
   if bio:
      await it_s6.update_profile(bio=bio)
   else:
      await it_s6.update_profile(bio="")
   if my_info.photo:
      photos = [p async for p in it_s6.get_chat_photos("me")]
      await it_s6.delete_profile_photos([p.file_id for p in photos[0:]])
      if c_photo:
         pass
      else:
         for photo_file in photo_files:
          photo_path = os.path.join("downloads", photo_file)
          if not c_photo:
             await it_s6.set_profile_photo(photo=photo_path)
   else:
      for photo_file in photo_files:
          photo_path = os.path.join("downloads", photo_file)
          if not c_photo:
             await it_s6.set_profile_photo(photo=photo_path)
   redis.delete(f'{it_s6.me.id}:clone_first_name')
   redis.delete(f'{it_s6.me.id}:clone_last_name')
   redis.delete(f'{it_s6.me.id}:clone_username')
   redis.delete(f'{it_s6.me.id}:clone_bio')
   redis.delete(f'{it_s6.me.id}:clone_c_photo')
   await eod(message, clone_msg4)
   import shutil
   shutil.rmtree('downloads')

back_button = types.InlineKeyboardMarkup(
            [[
             types.InlineKeyboardButton(b_button,callback_data="B_clo"),
             ]]
             )

@bot.on_callback_query(filters.regex('^b_clone'))
async def b_clone(client, callback_query):
    if callback_query.from_user.id != it_s6.me.id:
       return await bot.answer_callback_query(callback_query.id, text=c_me, show_alert=True)
    return await callback_query.edit_message_text(
        strings.HELP_CMD.format(module=__mod_name__, help=__help__),
        reply_markup=back_button)

@bot.on_callback_query(filters.regex('^B_clo'))
async def B_clo(client, callback_query):
    if callback_query.from_user.id != it_s6.me.id:
       return await bot.answer_callback_query(callback_query.id, text=c_me, show_alert=True)
    return await callback_query.edit_message_text(
        text="", 
        reply_markup=R_MENU, 
        parse_mode=enums.ParseMode.MARKDOWN
    )

__mod_name__ = "Clone"  
    
__help__ = f"""  

{SORUCE_EMJ} `{HNDLR}{clone_command}`
{clone_us}

{SORUCE_EMJ} `{HNDLR}{unclone_command}`
{unclone_us}

{My_User}
"""
    
    
string = {"module": __mod_name__, "help": __help__}   
MODULE.append(string)