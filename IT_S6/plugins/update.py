from IT_S6 import it_s6, bot, redis, My_User, version, HNDLR, SORUCE_EMJ, UPSTREAM_REPO_URL, MODULE
from pyrogram import filters, types, enums
from git import Repo
from git.exc import GitCommandError, InvalidGitRepositoryError, NoSuchPathError
from os import path, remove
from .__Help import R_MENU
from ..Langs import *
import asyncio, sys, subprocess, strings, config

requirements_path = path.join(
    path.dirname(path.dirname(path.dirname(__file__))), "requirements.txt"
)

async def gen_chlog(repo, diff):
    ch_log = ""
    d_form = "%d/%m/%y"
    for c in repo.iter_commits(diff):
        ch_log += (
            f"• [{c.committed_datetime.strftime(d_form)}]: {c.summary} <{c.author}>\n"
        )
    return ch_log

async def updateme_requirements():
    reqs = str(requirements_path)
    try:
        process = await asyncio.create_subprocess_shell(
            " ".join([sys.executable, "-m", "pip", "install", "-r", reqs]),
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        await process.communicate()
        return process.returncode
    except Exception as e:
        return repr(e)

def up_menu(chat_id):
    update_markup = types.InlineKeyboardMarkup(
        [[
            types.InlineKeyboardButton("Update Now", callback_data=f"up_{chat_id}"),
        ]]
    )
    return update_markup    

@bot.on_inline_query(filters.regex("^update$"))
async def up_inl(client, inline_query):
      await inline_query.answer(
        results=[
            types.InlineQueryResultArticle(
                title="it_s6",
                input_message_content=types.InputTextMessageContent(changelog_str),
                reply_markup=update_markup
            ),
           ],
        cache_time=1
        )
      
@bot.on_inline_query(filters.regex("^update_d$"))
async def upd_inl(client, inline_query):
      file = open("Update_Logs.txt", "w+")
      file.write(changelog_str)
      file.close()
      await inline_query.answer(
        results=[
            types.InlineQueryResultCachedDocument(
                document_file_id="Update_Logs.txt",
                title="it_s6",
                reply_markup=update_markup
            ),
           ],
        cache_time=1
        )
      remove("Update_Logs.txt")

@it_s6.on_message(filters.command("",HNDLR) & filters.me)
async def update(client, message):
    global changelog_str, update_markup, ups_rem, ac_br, repo, status
    update_markup = up_menu(message.chat.id)
    status = await message.edit(c_update)
    off_repo = UPSTREAM_REPO_URL
    try:
        repo = Repo()
    except NoSuchPathError as error:
        print(error)
        repo.__del__()
        return
    except GitCommandError as error:
        print(error)
        repo.__del__()
        return
    except InvalidGitRepositoryError:
        repo = Repo.init()
        origin = repo.create_remote("upstream", off_repo)
        origin.fetch()
        repo.create_head(
            "main",
            origin.refs["main"],
        )
        repo.heads["main"].set_tracking_branch(origin.refs["main"])
        repo.heads["main"].checkout(True)
    ac_br = repo.active_branch.name
    if ac_br != "main":
        repo.__del__()
        return
    try:
        repo.create_remote("upstream", off_repo)
    except BaseException:
        pass
    ups_rem = repo.remote("upstream")
    ups_rem.fetch(ac_br)
    changelog = await gen_chlog(repo, f"HEAD..upstream/{ac_br}")
    if changelog:
        changelog_str = update_msg1.format(SORUCE_EMJ, SORUCE_EMJ, version, SORUCE_EMJ, changelog)
        if len(changelog_str) > 4096:
            await status.delete()
            result = await it_s6.get_inline_bot_results(config.BOT_USER, query="update_d")
            sent_message = await it_s6.send_inline_bot_result(message.chat.id, result.query_id, result.results[0].id)
            message_id = sent_message.updates[0].id
            redis.hset('last_update_msg_ids', message.from_user.id, message_id)
        else:
            await status.delete()
            result = await it_s6.get_inline_bot_results(config.BOT_USER, query="update")
            sent_message = await it_s6.send_inline_bot_result(message.chat.id, result.query_id, result.results[0].id)
            message_id = sent_message.updates[0].id
            redis.hset('last_update_msg_ids', message.from_user.id, message_id)

    else:
        await status.edit(update_msg4)
        repo.__del__()
    return

back_button = types.InlineKeyboardMarkup(
            [[
             types.InlineKeyboardButton(b_button,callback_data="B_updat"),
             ]]
             )

@bot.on_callback_query(filters.regex('^b_update'))
async def b_update(client, callback_query):
    if callback_query.from_user.id != it_s6.me.id:
       return await bot.answer_callback_query(callback_query.id, text=c_me, show_alert=True)
    return await callback_query.edit_message_text(
        strings.HELP_CMD.format(module=__mod_name__, help=__help__),
        reply_markup=back_button)

@bot.on_callback_query(filters.regex('^B_updat'))
async def B_updat(client, callback_query):
    if callback_query.from_user.id != it_s6.me.id:
       return await bot.answer_callback_query(callback_query.id, text=c_me, show_alert=True)
    return await callback_query.edit_message_text(
        text="", 
        reply_markup=R_MENU, 
        parse_mode=enums.ParseMode.MARKDOWN
    )

@bot.on_callback_query(filters.regex("up"))
async def up(client, callback_query):
    if callback_query.from_user.id != it_s6.me.id:
        return await bot.answer_callback_query(callback_query.id, text=c_me, show_alert=True)
    chat_id = int(callback_query.data.split("_")[1])
    last_update_msg_ids = redis.hget('last_update_msg_ids', chat_id)
    await it_s6.delete_messages(chat_id, int(last_update_msg_ids))
    try:
        ups_rem.pull(ac_br)
    except GitCommandError:
        repo.git.reset("--hard", "FETCH_HEAD")
    redis.set("Restart", chat_id)
    r = await it_s6.send_message(chat_id, update_msg3)
    redis.set('last_restart_msg_ids', int(r.id))
    await updateme_requirements()
    redis.set("Restart", chat_id)
    await asyncio.sleep(0.5)
    subprocess.Popen([sys.executable, "-B", "-m", "IT_S6"], close_fds=True)
    sys.exit(0)

__mod_name__ = "Update"  
    
__help__ = f"""  

{SORUCE_EMJ} `{HNDLR}{update_command}`
{update_us}

{My_User}
"""  
    
string = {"module": __mod_name__, "help": __help__}   
MODULE.append(string)
