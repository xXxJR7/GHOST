from pyrogram import filters, types
from IT_S6 import it_s6, bot, redis, HNDLR
from ..Langs import *
import config

help_photo_url = "" or redis.get("Help_Pic")

R_MENU = types.InlineKeyboardMarkup(
            [[
             types.InlineKeyboardButton(h9_,callback_data="b_restart"),
             types.InlineKeyboardButton(h10_,callback_data="b_update"),
             ],
             [
             types.InlineKeyboardButton(h11_,callback_data="b_play"),
             types.InlineKeyboardButton(h12_,callback_data="b_clone"),
             ],
             [
             types.InlineKeyboardButton(h13_,callback_data="b_telegraph"),
             types.InlineKeyboardButton(h14_,callback_data="b_prevent"),
             ],
             [
             types.InlineKeyboardButton(h15_,callback_data="b_mention"),
             ],
             [
             types.InlineKeyboardButton(h_p,callback_data="b_previous2"),
             types.InlineKeyboardButton(h_c,callback_data="b_close"),
             types.InlineKeyboardButton(h_n,callback_data="b_next2"),
             ]]
             )

MENU = types.InlineKeyboardMarkup(
            [[
             types.InlineKeyboardButton(h1_,callback_data="b_mute"),
             types.InlineKeyboardButton(h2_,callback_data="b_ban"),
             ],
             [
             types.InlineKeyboardButton(h3_,callback_data="b_autoname"),
             types.InlineKeyboardButton(h4_,callback_data="b_id"),
             ],
             [
             types.InlineKeyboardButton(h5_,callback_data="b_logs"),
             types.InlineKeyboardButton(h6_,callback_data="b_locks"),
             ],
             [
             types.InlineKeyboardButton(h7_,callback_data="b_PMSecurity"),
             types.InlineKeyboardButton(h8_,callback_data="b_must_join"),
             ],
             [
             types.InlineKeyboardButton(h_p,callback_data="b_previous1"),
             types.InlineKeyboardButton(h_c,callback_data="b_close"),
             types.InlineKeyboardButton(h_n,callback_data="b_next1"),
             ]]
             )

RE_MENU = types.InlineKeyboardMarkup(
            [[
             types.InlineKeyboardButton(h_o,callback_data="b_open")
             ]])

@bot.on_callback_query(filters.regex('^b_previous2'))
async def b_previous2(client, callback_query):
    if callback_query.from_user.id != it_s6.me.id:
       return await bot.answer_callback_query(callback_query.id, text=c_me, show_alert=True)
    return await callback_query.edit_message_text(
        "",
        reply_markup=MENU)

@bot.on_callback_query(filters.regex('^b_previous1'))
async def b_previous1(client, callback_query):
    if callback_query.from_user.id != it_s6.me.id:
       return await bot.answer_callback_query(callback_query.id, text=c_me, show_alert=True)
    return await callback_query.edit_message_text(
        "",
        reply_markup=R_MENU)

@bot.on_callback_query(filters.regex('^b_next1'))
async def b_next1(client, callback_query):
    if callback_query.from_user.id != it_s6.me.id:
       return await bot.answer_callback_query(callback_query.id, text=c_me, show_alert=True)
    return await callback_query.edit_message_text(
        "",
        reply_markup=R_MENU)

@bot.on_callback_query(filters.regex('^b_next2'))
async def b_next2(client, callback_query):
    if callback_query.from_user.id != it_s6.me.id:
       return await bot.answer_callback_query(callback_query.id, text=c_me, show_alert=True)
    return await callback_query.edit_message_text(
        "",
        reply_markup=MENU)

@bot.on_callback_query(filters.regex('^b_close'))
async def b_close(client, callback_query):
    if callback_query.from_user.id != it_s6.me.id:
       return await bot.answer_callback_query(callback_query.id, text=c_me, show_alert=True)
    return await callback_query.edit_message_text(
        close_menu,
        reply_markup=RE_MENU)

@bot.on_callback_query(filters.regex('^b_open'))
async def b_open(client, callback_query):
    if callback_query.from_user.id != it_s6.me.id:
       return await bot.answer_callback_query(callback_query.id, text=c_me, show_alert=True)
    return await callback_query.edit_message_text(
        "",
        reply_markup=MENU)

@bot.on_inline_query(filters.regex("sa3ed"))
async def help_cmds(client, inline_query):
    if not help_photo_url:
        return await inline_query.answer(
            results=[
                types.InlineQueryResultArticle(
                   title="it_s6",
                   input_message_content=types.InputTextMessageContent(h),
                   reply_markup=MENU
                   ),
                ],
            cache_time=1
            )
    await inline_query.answer(
        results=[
            types.InlineQueryResultPhoto(
                photo_url=help_photo_url,
                photo_width=1000,
                photo_height=1000,
                title="it_s6",
                description="",
                reply_markup=MENU
            ),
        ],
        cache_time=1
    )

@it_s6.on_message(filters.command(help_command, HNDLR) & filters.me)
async def commands(client, message):
    from ..Helper import sod
    await message.delete()
    try:
        result = await it_s6.get_inline_bot_results(
            config.BOT_USER,
            "sa3ed"
        )

        await it_s6.send_inline_bot_result(
            message.chat.id,
            query_id=result.query_id,
            result_id=result.results[0].id,
            disable_notification=True,
        )
    except:
        await sod(message.chat.id, c_inline)
