# -*- coding: utf-8 -*-
#pip install aiogram 
#pip install openai 
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
import asyncio
import openai
import json
import re
from aiogram.types import InputMediaPhoto
openai.api_key='1申請的key'
openai.api_base = 'https://chimeragpt.adventblocks.cc/api/v1'
logging.basicConfig(level=logging.INFO)
API_TOKEN = 'bot 令牌'
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
    item2 = types.KeyboardButton('/draw')
    keyboard.add(item0, item1, item2)
    await message.reply(f'你好：{user_name},TG:{user_id}！\n歡迎使用機器人！', reply_markup=keyboard)
#繪畫
@dp.message_handler(commands='draw')
async def handle_chat(message: types.Message):
    userMessage=message.text[5:len(message.text)].strip()
    if(len(userMessage)>0):
        response = openai.Image.create(
            prompt=userMessage,
            n=10,  # images count
            size="1024x1024"
        )    
        responseimg=json.dumps(response["data"])
        mediaphoto=[InputMediaPhoto(media=img["url"]) for img in eval(responseimg)]
        await message.reply_media_group(media=mediaphoto)
    else:
        await message.reply("請輸入描述詞，目前只支持英語。\n格式：/draw description")

#chat with chatgpt
@dp.message_handler(commands='chat')
async def handle_chat(message: types.Message):
    userMessage=message.text[5:len(message.text)].strip()
    try:
        reply=await message.reply("正在思考中……")
        sendmsg=""
        response = openai.ChatCompletion.create(
            model='gpt-4',
            messages=[
                {'role': 'user', 'content': userMessage},
            ],
            stream=True
        )
        
        
        for chunk in response:
            msg=chunk.choices[0].delta.get("content", "")
            if(len(msg)>0):
                sendmsg=sendmsg+msg  
            if(len(sendmsg) % 30 == 1):
                await bot.edit_message_text(sendmsg,chat_id=reply.chat.id,message_id=reply.message_id)
        sendmsg=sendmsg+"\n\n   回復完畢。"
        #print(sendmsg)     
        await bot.edit_message_text(sendmsg,chat_id=reply.chat.id,message_id=reply.message_id)      
    except openai.error.APIError as e:
        detail_pattern = re.compile(r'{"detail":"(.*?)"}')
        match = detail_pattern.search(e.user_message)
        if match:
            error_message = match.group(1)
        else:
            error_message=e.user_message
        await bot.edit_message_text(error_message,chat_id=reply.chat.id,message_id=reply.message_id)

async def send_message(chat_id, text):
    await bot.send_message(chat_id=chat_id, text=text)

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(send_message(chat_id=chat_id, text="機器人已就緒！"))
    executor.start_polling(dp, skip_updates=True)
