#!/usr/bin/env python3

import aioredis
from aiohttp import web
from views import SendMessage, SendChatAction, BotApi, ChatApi, UserApi


async def create_redis(app):

    app['redis_client'] = await aioredis.create_redis_pool(
        'redis://localhost', minsize=5, maxsize=10)


app = web.Application()

app.on_startup.append(create_redis)

app.router.add_view('/user', UserApi)
app.router.add_view('/user/{username}', UserApi)
app.router.add_view('/chat', ChatApi)
app.router.add_view('/chat/{chat_id}', ChatApi)
app.router.add_view('/bot', BotApi)
app.router.add_view('/bot/{botname}', BotApi)
app.router.add_view('/bot{token}/sendChatAction', SendChatAction)
app.router.add_view('/bot{token}/sendMessage', SendMessage)

web.run_app(app)
