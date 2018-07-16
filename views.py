#!/usr/bin/env python3

import json
import random
from aiohttp import web
from utils import create_empty_response
from models import Chat, Bot, User
from tasks import start_chat, random_replay, delay


class BotApi(web.View):

    async def post(self):

        request_json = await self.request.json()
        bot = await Bot(self.request.app).create(request_json)
        return web.json_response({'bot': bot}, status=201)


class UserApi(web.View):

    async def post(self):

        request_json = await self.request.json()
        user = await User(self.request.app).create(request_json)
        return web.json_response({'user': user}, status=201)


class ChatApi(web.View):

    async def post(self):

        request_json = await self.request.json()
        chat = await Chat(self.request.app).create(request_json)
        self.request.app.loop.create_task(start_chat(self.request.app, chat=chat))
        return web.json_response({'chat': chat}, status=201)


class SendChatAction(web.View):
    """ https://core.telegram.org/bots/api#sendchataction """

    async def post(self):
        return web.json_response(create_empty_response())


class SendMessage(web.View):
    """ https://core.telegram.org/bots/api#sendmessage """

    def extract_keyboard(self, request_post):

        if 'reply_markup' in request_post and request_post['reply_markup']:
            reply_markup = json.loads(request_post['reply_markup'])
            return reply_markup.get('keyboard')

    async def post(self):

        request_post = await self.request.post()
        chat = await Chat(self.request.app).get(request_post['chat_id'])

        keyboard = self.extract_keyboard(request_post)
        if keyboard:
            self.request.app.loop.create_task(
                delay(
                    random_replay(self.request.app, chat, keyboard),
                    countdown=random.randint(1, 10)
                )
            )

        return web.json_response(create_empty_response())
