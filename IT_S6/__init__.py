from pyrogram import Client, types
from pyrogram.errors import AuthKeyUnregistered
from time import sleep
import config, asyncio, redis, sys, requests, random, os, subprocess

REDIS_INFO = f"redis://:{config.REDIS_PASSWORD}@{config.REDIS_URL}"
redis = redis.from_url(REDIS_INFO, decode_responses=True)

SESSION = redis.get("SESSION") or config.SESSION

it_s6=Client(
    "xXx_JR",
    config.API_ID,
    config.API_HASH,
    in_memory=True,
    session_string=SESSION
)

bot = Client(
    "xXx_JR",
    config.API_ID,
    config.API_HASH,
    bot_token=config.BOT_TOKEN,
)

MODULE = []
UPSTREAM_REPO_URL = "https://github.com/sa3ed266it/ITALIA.git"
LANG = redis.get("LANGUAGE") or config.LANGUAGE
SORUCE_EMJ = redis.get("SORUCE_EMJ") or "•"
HNDLR = redis.get("HNDLR") or "."
if HNDLR == "NO_HNDLR":
    HNDLR = ""
My_User = "@xXx_JR"

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

if not SESSION:
   print("SESSION Not Found")
   gen_session1()

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
