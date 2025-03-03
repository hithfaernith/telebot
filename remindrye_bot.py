import os
from dotenv import load_dotenv
from datetime import time, timezone, timedelta
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
import asyncio
import requests
from datetime import datetime
load_dotenv()

# API endpoint for two-hour weather forecast
API_URL = "https://api-open.data.gov.sg/v2/real-time/api/two-hr-forecast"

# Query parameters (You might need to adjust based on API requirements, e.g., location)
params = {
    "location": "Queenstown"  # Ensure the location is specified correctly if required by the API
}

BOT_TOKEN = os.environ.get('BOT_TOKEN')
CHAT_ID = os.environ.get('CHAT_TOKEN')
tz  = timezone(timedelta(hours=8))

def get_weather_data():
    # Send GET request to the API
    response = requests.get(API_URL, params=params)

    # Check if the request was successful
    if response.status_code == 200:
        data = response.json()
        if data["code"] == 0: 
            location = data["data"]["items"][0]["forecasts"][30]["area"]
            forecast = data["data"]["items"][0]["forecasts"][30]["forecast"]
            res = f"Weather in {location}: {forecast}\n"
            dt_object = datetime.fromisoformat(data["data"]["items"][0]["update_timestamp"])
            human_readable = dt_object.strftime('%d %B %Y, %H:%M:%S')
            res += f"Data updated on {human_readable}"
            return res
        else:
            return "Weather update timestamp not available."
    else:
        return f"Failed to retrieve data. Status code: {response.status_code}"

async def start(update:Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hello!")

async def lunch(context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=CHAT_ID, text="pls go eat")

async def noot(context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=CHAT_ID, text="N00T N00T")

async def queenstown_weather(context: ContextTypes.DEFAULT_TYPE):
    weather_info = get_weather_data()
    await context.bot.send_message(chat_id=CHAT_ID, text=f"{weather_info}\n")

async def weather_update(update: Update, context: ContextTypes.DEFAULT_TYPE):
    weather_info = get_weather_data()
    await update.message.reply_text(f"{weather_info}\n")

def main():
    application = Application.builder().token(BOT_TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("weatherupdate", weather_update))
    job_queue = application.job_queue
    job_queue.run_daily(queenstown_weather, time=time(hour=8, minute=50, second=0, tzinfo=tz))
    job_queue.run_daily(lunch, time=time(hour=12, minute=00, second=0, tzinfo=tz))
    job_queue.run_daily(queenstown_weather, time=time(hour=17, minute=50, second=0, tzinfo=tz))
    job_queue.run_daily(noot, time=time(hour=19, minute=00, second=0, tzinfo=tz))
    application.run_polling()

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())