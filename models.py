#!/usr/bin/env python3


class NotFound(Exception):
    pass


class Bot:

    def __init__(self, app):
        self.app = app

    async def create(self, data):
        key = 'bots:%s' % data['botname']
        data['id'] = await self.app['redis_client'].incr('last_bot_id')
        await self.app['redis_client'].hmset_dict(key, data)
        return data

    async def get(self, botname):
        key = 'bots:%s' % botname
        data = await self.app['redis_client'].hgetall(key, encoding='ascii')
        if not data:
            raise NotFound(botname)
        return data


class User:

    def __init__(self, app):
        self.app = app

    async def create(self, data):
        key = 'users:%s' % data['username']
        data['id'] = await self.app['redis_client'].incr('last_user_id')
        await self.app['redis_client'].hmset_dict(key, data)
        return data

    async def get(self, username):
        key = 'users:%s' % username
        data = await self.app['redis_client'].hgetall(key, encoding='ascii')
        if not data:
            raise NotFound(username)
        return data


class Chat:

    def __init__(self, app):
        self.app = app

    async def create(self, data):
        data['id'] = await self.app['redis_client'].incr('last_chat_id')
        key = 'chats:%s' % data['id']
        await self.app['redis_client'].hmset_dict(key, data)
        return data

    async def get(self, chat_id):
        key = 'chats:%s' % chat_id
        data = await self.app['redis_client'].hgetall(key, encoding='ascii')
        data['id'] = int(data['id'])
        return data

    async def incr_update_id(self, chat_id):
        key = 'chats:%s' % id
        return await self.app['redis_client'].hincrby(key, 'update_id', 1)
