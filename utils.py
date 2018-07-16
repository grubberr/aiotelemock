#!/usr/bin/env python3

import time
from models import Chat

async def create_fake_message(app, user, chat, text):

    update_id = await Chat(app).incr_update_id(chat['id'])

    return {
        'message': {
            'from': {
                'username': user['username'],
                'first_name': user['first_name'],
                'id': user['id']
            },
            'text': text,
            'chat': {
                'username': user['username'],
                'first_name': user['first_name'],
                'type': 'private',
                'id': chat['id']
            },
            'date': int(time.time()),
            'message_id': 1
        },
        'update_id': update_id
    }

def create_empty_response():
    return {'ok': True, 'result': []}
