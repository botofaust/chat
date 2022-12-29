import datetime
import json

from asgiref.sync import sync_to_async
from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer

from .models import ChatMessage, ChatUser, ChatRoom


# В CHAT_CLIENTS будем хранить подключенных сокетов для каждого чата:
#     {chatroom1.id: [ChatConsumers....],
#      chatroom2.id: [ChatConsumers....],
#      ... }

CHAT_CLIENTS = {}


class ChatConsumer(AsyncWebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(args, kwargs)
        self.chat_id = None
        self.user_id = None

    @database_sync_to_async
    def create_message(self, message):
        owner = ChatUser.objects.get(pk=self.user_id)
        chat = ChatRoom.objects.get(pk=self.chat_id)
        ChatMessage.objects.create(
            text=message,
            chat=chat,
            owner=owner)

    @database_sync_to_async
    def get_last_messages(self, count=10):
        messages = ChatMessage.objects.filter(chat=self.chat_id).order_by('-created_at')[:count]
        msg_arr = []
        for msg in reversed(messages):
            msg_arr.append(msg.get_text_for_chat())
        return msg_arr

    async def connect(self):
        self.user_id = self.scope["user"].id
        self.chat_id = self.scope['url_route']['kwargs']['pk']
        if self.chat_id not in CHAT_CLIENTS.keys():
            CHAT_CLIENTS[self.chat_id] = []
        CHAT_CLIENTS[self.chat_id].append(self)
        print('add...', CHAT_CLIENTS)
        await self.accept()
        await self.send_last_messages()

    async def disconnect(self, close_code):
        CHAT_CLIENTS[self.chat_id].remove(self)

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        await self.create_message(text_data_json['message'])

    @staticmethod
    async def send_to_chat(chat_id, message):
        print('1...', CHAT_CLIENTS, '2...', chat_id)
        if chat_id not in CHAT_CLIENTS.keys():
            return
        text_data = json.dumps({'message': message})
        for socket in CHAT_CLIENTS[chat_id]:
            await socket.send(text_data)

    async def send_last_messages(self):
        messages = await self.get_last_messages()
        for message in messages:
            text_data = json.dumps({'message': message})
            await self.send(text_data)
