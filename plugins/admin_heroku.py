# Made by @codexnano from scratch.
# If you find any bugs, please let us know in the channel updates.
# You can 'git pull' to stay updated with the latest changes.

from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup as KM, InlineKeyboardButton as KB
from services.heroku import Heroku
from config import Config
import logging
import io
log = logging.getLogger(__name__)
def owner_only(_, __, m):
    return m.from_user and m.from_user.id in Config.OWNER_ID
owner_filter = filters.create(owner_only)
@Client.on_message(filters.command("heroku") & filters.private & owner_filter)
async def heroku_panel_cmd(c, m):
    await show_heroku_panel(m)
async def show_heroku_panel(msg, edit=False):
    app, err = await Heroku.get_app()
    if err:
        txt = f"<b>[X] Heroku Error</b>\n\n<code>{err}</code>"
        btns = KM([[KB("↻ Try Again", "h_panel")]])
    else:
        name = app.get('name')
        status = app.get('web_url')
        updated = app.get('updated_at', '').replace('T', ' ').replace('Z', '')
        txt = (
            "<b>┌─ HEROKU PANEL ─┐</b>\n\n"
            f"│ <b>App:</b> <code>{name}</code>\n"
            f"│ <b>Updated:</b> <code>{updated}</code>\n"
            "└───────────────────\n\n"
            "<i>Select an action below:</i>"
        )
        btns = KM([
            [KB("↻ Dynos", "h_dynos"), KB("⌬ Logs", "h_logs")],
            [KB("◆ Config Vars", "h_vars")],
            [KB("↻ Restart All", "h_rst_all")],
            [KB("✕ Close", "close")]
        ])
    if edit:
        await msg.edit(txt, reply_markup=btns)
    else:
        await msg.reply(txt, reply_markup=btns)
@Client.on_callback_query(filters.regex("^h_panel") & owner_filter)
async def h_panel_cb(c, q):
    await show_heroku_panel(q.message, edit=True)
    await q.answer()
@Client.on_callback_query(filters.regex("^h_dynos") & owner_filter)
async def h_dynos_cb(c, q):
    dynos, err = await Heroku.get_dynos()
    if err: return await q.answer(f"Error: {err}", show_alert=True)
    txt = "<b>┌─ DYNOS ─┐</b>\n\n"
    if not dynos:
        txt += "│ <i>No active dynos</i>\n"
    else:
        for d in dynos:
            txt += f"│ <b>{d['name']}</b>: <code>{d['state']}</code>\n"
    txt += "└───────────"
    btns = KM([[KB("◂ Back", "h_panel")]])
    await q.message.edit(txt, reply_markup=btns)
    await q.answer()
@Client.on_callback_query(filters.regex("^h_rst_all") & owner_filter)
async def h_rst_all_cb(c, q):
    await q.answer("Restarting all dynos...", show_alert=False)
    _, err = await Heroku.restart_all()
    if err:
        await q.answer(f"Fail: {err}", show_alert=True)
    else:
        await q.answer("Success! App is restarting.", show_alert=True)
    await show_heroku_panel(q.message, edit=True)
@Client.on_callback_query(filters.regex("^h_logs") & owner_filter)
async def h_logs_cb(c, q):
    await q.answer("Fetching logs...")
    logs, err = await Heroku.get_logs(lines=100)
    if err:
        return await q.answer(f"Error: {err}", show_alert=True)
    f = io.BytesIO(logs.encode())
    f.name = "heroku_logs.txt"
    await q.message.reply_document(f, caption="<b>[+] Heroku Logs (Last 100 lines)</b>")
    await q.answer()
@Client.on_callback_query(filters.regex("^h_vars") & owner_filter)
async def h_vars_cb(c, q):
    vars, err = await Heroku.get_vars()
    if err: return await q.answer(f"Error: {err}", show_alert=True)
    txt = "<b>┌─ CONFIG VARS ─┐</b>\n\n"
    keys = list(vars.keys())
    for k in keys[:15]:
        txt += f"│ <code>{k}</code>\n"
    if len(keys) > 15:
        txt += f"│ <i>... +{len(keys)-15} more</i>\n"
    txt += "└───────────────"
    btns = KM([[KB("◂ Back", "h_panel")]])
    await q.message.edit(txt, reply_markup=btns)
    await q.answer()
