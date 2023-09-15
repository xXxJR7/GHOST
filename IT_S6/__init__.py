from pyrogram import Client, types
from pyrogram.errors import AuthKeyUnregistered
from time import sleep
import config, asyncio, redis, sys, requests, random, os, subprocess

REDIS_INFO = f"redis://:{config.REDIS_PASSWORD}@{config.REDIS_URL}"
redis = redis.from_url(REDIS_INFO, decode_responses=True)

SESSION1 = redis.get("SESSION1") or config.SESSION1

it_s6=Client(
    "IT_S6",
    api_id = config.API_ID,
    api_hash = config.API_HASH,
    in_memory=True,
    session_string = SESSION1
)

bot = Client(
    "IT_S6",
    config.API_ID,
    config.API_HASH,
    bot_token=config.BOT_TOKEN,
)

it_s6_music=Client(
    "IT_S6_MUSIC",
    api_id = config.API_ID,
    api_hash = config.API_HASH,
    in_memory=True,
    session_string = config.SESSION2
)

from pytgcalls import PyTgCalls
app = PyTgCalls(it_s6_music)

MODULE = []
UPSTREAM_REPO_URL = "https://github.com/sa3ed266it/IT_S6.git"
LANG = redis.get("LANGUAGE") or config.LANGUAGE
SORUCE_EMJ = redis.get("SORUCE_EMJ") or "•"
HNDLR = redis.get("HNDLR") or "."
if HNDLR == "NO_HNDLR":
    HNDLR = ""
My_User = "@IT_S6"

if not config.API_ID:
   print("API_ID Not Found")
   sys.exit()

if not config.API_HASH:
   print("API_HASH Not Found")
   sys.exit()

def gen_session1():
   print("Generating New One ...")
   client = Client("memory", config.API_ID, config.API_HASH)
   client.connect()
   phone_number = input("Your Phone Number : ")
   code = client.send_code(phone_number)
   phone_code_msg = input("Type Registration Code : ")
   try:
        print("Logging  ...")
        client.sign_in(phone_number, code.phone_code_hash, phone_code_msg)
   except:
        password = input("Type Your Two Factor Authentication Password : ")
        client.check_password(password=password)
   string_session = client.export_session_string()
   redis.set("SESSION1", string_session)
   subprocess.Popen([sys.executable, "-B", "-m", "IT_S6"], close_fds=True)
   sys.exit(0)

if not SESSION1:
   print("SESSION1 Not Found")
   gen_session1()

if not config.SESSION2:
   app = PyTgCalls(it_s6)

if not config.REDIS_URL:
   print("REDIS_URL Not Found")
   sys.exit()

if not config.REDIS_PASSWORD:
   print("REDIS_PASSWORD Not Found")
   sys.exit()

if not config.TZ:
   config.TZ = "Africa/Cairo"

if not config.LANGUAGE:
   config.LANGUAGE = "en"
   
if not config.BOT_TOKEN:
   print("BOT_TOKEN Not Found")
   sys.exit()
  

def get_bot_information():
    bot_inf = requests.get(
        "https://api.telegram.org/bot" + config.BOT_TOKEN + "/getme")
    bot_info = bot_inf.json()
    result = bot_info["result"]
    bot_username = result["username"]
    return bot_username

if not config.BOT_USER:
   config.BOT_USER = get_bot_information()

LOG = redis.get("LOGS") or config.LOGS
if not LOG:
   print("LOG GROUP Not Found")
   it_s6.start()
   photos = random.choice(["https://images.alphacoders.com/107/1071645.jpg",
                        "https://www.pixel4k.com/wp-content/uploads/2019/03/spiderman-miles-lost-in-space-4k_1553071367.jpg",
                        "https://free4kwallpapers.com/uploads/originals/2022/04/20/rubiks-cube-digital-art-wallpaper.jpg",
                        "https://wallpapercave.com/wp/wp2577314.jpg",
                        "https://free4kwallpapers.com/uploads/originals/2020/09/11/firewatch-dark-version-wallpaper.jpg"])
   print("Making GroupLog ...")
   s4 =  it_s6.create_supergroup(
       title="IT_S6_LOGS",
       description="This is Group Log For You")
   sleep(0.3)
   redis.set("LOGS", int(s4.id))
   it_s6.add_chat_members(s4.id, "@"+config.BOT_USER)
   sleep(0.3)
   it_s6.promote_chat_member(s4.id, "@"+config.BOT_USER, types.ChatPrivileges(
            can_manage_chat=True,
            can_delete_messages=True,
            can_manage_video_chats=True,
            can_restrict_members=True,
            can_promote_members=True,
            can_change_info=True,
            can_post_messages=True,
            can_edit_messages=True,
            can_invite_users=True,
            can_pin_messages=True
            ))
   sleep(0.3)
   it_s6.set_administrator_title(s4.id, "@"+config.BOT_USER, title="Assistant")
   sleep(0.3)
   response = requests.get(photos)
   with open("sa3ed.jpg", "wb") as ph:
          ph.write(response.content)
   it_s6.set_chat_photo(s4.id, photo="sa3ed.jpg")
   sleep(0.3)
   os.remove("sa3ed.jpg")
   subprocess.Popen([sys.executable, "-B", "-m", "IT_S6"], close_fds=True)
   sys.exit(0)

async def gen_session2():
   print("Generating New One ...")
   client = Client("memory", config.API_ID, config.API_HASH)
   await client.connect()
   phone_number = input("Your Phone Number : ")
   code = await client.send_code(phone_number)
   phone_code_msg = input("Type Registration Code : ")
   try:
        print("Logging  ...")
        await client.sign_in(phone_number, code.phone_code_hash, phone_code_msg)
   except:
        password = input("Type Your Two Factor Authentication Password : ")
        await client.check_password(password=password)
   string_session = await client.export_session_string()
   redis.set("SESSION1", string_session)
   subprocess.Popen([sys.executable, "-B", "-m", "IT_S6"], close_fds=True)
   sys.exit(0)

with open("version.txt") as ver:
    version = ver.read().strip()

async def it_s6_startup():
   try:
    await it_s6.start()
   except AuthKeyUnregistered :
      print("Session Key Expired")
      await gen_session2()

asyncio.get_event_loop().run_until_complete(it_s6_startup())
