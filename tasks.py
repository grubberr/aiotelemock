#!/usr/bin/env python3

import random
import asyncio
import aiohttp
from utils import create_fake_message
from models import Bot, User


async def delay(task, countdown):
    await asyncio.sleep(countdown)
    return await task


async def start_chat(app, chat):

    bot = await Bot(app).get(chat['botname'])
    user = await User(app).get(chat['username'])
    response = await create_fake_message(app, user, chat, '/start')

    async with app['client_session'].post(bot['callback'], json=response) as resp:
        await resp.text()


async def random_replay(app, chat, keyboard):

    answer = random.choice(keyboard[0])

    bot = await Bot(app).get(chat['botname'])
    user = await User(app).get(chat['username'])
    response = await create_fake_message(app, user, chat, answer)

    async with app['client_session'].post(bot['callback'], json=response) as resp:
        await resp.text()
