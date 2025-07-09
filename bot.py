from pyrogram import Client, filters
from config import API_ID, API_HASH, BOT_TOKEN, OWNER_ID, AUTH_USERS
from helper import readable_size
from pyrogram.types import Message
import aiohttp
import os

bot = Client("fs_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

@bot.on_message(filters.command("start") & filters.private)
async def start(_, m: Message):
    await m.reply("📁 Send a direct link or upload a file.")

@bot.on_message(filters.private & filters.user(AUTH_USERS) & filters.text)
async def download_url(_, m: Message):
    url = m.text.strip()
    if not url.startswith("http"):
        return await m.reply("❌ Send a valid HTTP/HTTPS link.")
    msg = await m.reply("⏳ Downloading...")
    filename = url.split("/")[-1].split("?")[0]
    try:
        async with aiohttp.ClientSession() as s:
            async with s.get(url) as r:
                data = await r.read()
                with open(filename, "wb") as f:
                    f.write(data)
        await msg.edit("✅ Uploading...")
        await m.reply_document(filename, caption=f"`{filename}`")
        os.remove(filename)
        await msg.delete()
    except Exception as e:
        await msg.edit(f"❌ Error: {e}")

@bot.on_message(filters.document & filters.private)
async def file_info(_, m: Message):
    d = m.document
    size = readable_size(d.file_size)
    await m.reply(f"📄 `{d.file_name}` — {size}")

bot.run()

