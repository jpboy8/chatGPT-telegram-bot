import os
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from dotenv import load_dotenv
import openai


load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")
bot = Bot(token=os.getenv('API_BOT'))
dp = Dispatcher(bot)


@dp.message_handler(commands=['start', 'help'])
async def commands_start(message: types.Message):
    await bot.send_message(message.from_user.id, 'Write something you want to know')


@dp.message_handler()
async def bot_message(message: types.Message):
    try:
        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=message.text,
            temperature=0.5,
            max_tokens=3800,
            top_p=1.0,
            frequency_penalty=0.5,
            presence_penalty=0.0,
        )
        await bot.send_message(message.from_user.id,
                               response['choices'][0]['text'])
    except Exception as e:
        print(e)
        await bot.send_message(message.from_user.id,
                               'The server had an error while processing your request. Sorry about that! Try later')

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
