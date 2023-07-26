# -*- coding: utf-8 -*-
#pip install aiogram 
#pip install openai 
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
import asyncio
import openai
openai.api_key='1申請的key'
openai.api_base = 'https://chimeragpt.adventblocks.cc/api/v1'
logging.basicConfig(level=logging.INFO)
API_TOKEN = 'bot token'
bot = Bot(token=API_TOKEN, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot)
global chat_id
chat_id=11111111 #默認的tgID
@dp.message_handler(commands='start')
async def handle_start(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    user_id=message.from_id
    user_name=message.from_user.full_name
    item0 = types.KeyboardButton('/start')
    item1 = types.KeyboardButton('/chat')
    keyboard.add(item0, item1)
    await message.reply(f'你好：{user_name},TG:{user_id}！\n歡迎使用機器人！', reply_markup=keyboard)
#chat with chatgpt
@dp.message_handler(commands='chat')
async def handle_chat(message: types.Message):
    userMessage=message.text[5:len(message.text)].strip()
    response = openai.ChatCompletion.create(
        model='gpt-4',
        messages=[
            {'role': 'user', 'content': userMessage},
        ],
        stream=True
    )
    reply=await message.reply("正在思考……")
    sendmsg=""
    
    for chunk in response:
        msg=chunk.choices[0].delta.get("content", "")
        if(len(msg)>0):
            sendmsg=sendmsg+msg  
        if(len(sendmsg) % 15 == 1):
            await bot.edit_message_text(sendmsg,chat_id=reply.chat.id,message_id=reply.message_id)
    sendmsg=sendmsg+"\n回復完畢"
    #print(sendmsg)     
    await bot.edit_message_text(sendmsg,chat_id=reply.chat.id,message_id=reply.message_id)      

async def send_message(chat_id, text):
    await bot.send_message(chat_id=chat_id, text=text)

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(send_message(chat_id=chat_id, text="機器人已就緒！"))
    executor.start_polling(dp, skip_updates=True)
