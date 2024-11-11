import os
from dotenv import load_dotenv
from datetime import time, timezone, timedelta
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
import asyncio

load_dotenv()

BOT_TOKEN = os.environ.get('BOT_TOKEN')
CHAT_ID = os.environ.get('CHAT_TOKEN')
tz  = timezone(timedelta(hours=8))

async def start(update:Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hello!")

async def lunch(context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=CHAT_ID, text="pls go eat")

async def noot(context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=CHAT_ID, text="N00T N00T")

def main():
    application = Application.builder().token(BOT_TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    job_queue = application.job_queue
    job_queue.run_daily(lunch, time=time(hour=12, minute=00, second=0, tzinfo=tz))
    job_queue.run_daily(noot, time=time(hour=21, minute=35, second=0, tzinfo=tz))
    application.run_polling()

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())