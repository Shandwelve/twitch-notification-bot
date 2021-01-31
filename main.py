from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from config import *
import asyncio
import requests

bot = Bot(token=TOKEN)
dispatcher = Dispatcher(bot)
stream_start = False


async def check_stream(wait_for: int):
    global stream_start
    while True:
        await asyncio.sleep(wait_for)
        stream = get_twitch_request()

        if stream != stream_start:
            stream_start = stream
            message = "Slavik Podrubil" if stream_start else "Slavik Ofnul"
            await bot.send_message(1007765065, message, disable_notification=True)


def get_twitch_request() -> bool:
    headers = {
        'client-id': CLIENT_ID,
        'Authorization': "Bearer {}".format(ACCESS_TOKEN)
    }
    params = {'user_login': USERNAME}
    response = requests.get(URL, headers=headers, params=params)

    return response.json()['data'][0]['type'] == 'live'

async def on_start(x):
    asyncio.create_task(check_stream(5))

if __name__ == '__main__':
    executor.start_polling(dispatcher, on_startup=on_start)
