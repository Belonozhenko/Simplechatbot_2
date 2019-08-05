
from channels.generic.websocket import AsyncWebsocketConsumer
import json
from .models import Message
from django.core import serializers
from django.contrib.auth import get_user_model
User = get_user_model()


class ChatConsumer(AsyncWebsocketConsumer):
    #fetching last 100 messages
    async def fetch_messages(self, data):
        messages = Message.last_100_messages(data)

        curnt_user = self.scope["user"]
        if messages:
            for message in messages:
                await self.channel_layer.group_send(
                    self.room_group_name,
                    {
                        'type': 'chat_message',
                        'message': message.content,
                        'user': str(message.autor),
                        'conecting_user': str(curnt_user),
                        'is_history': 'history',

                    }
                )

            #return result

           # t = self.messages_to_json(content)
           # self.send_chat_message(messages)

    #convert messages from DB to acceptable format
    def messages_to_json(self, messages):
        result = []
        for message in messages:
            result.append(self.message_to_json(message))
        return result



    #convert single message to JSON
    def message_to_json(self, message):
        return {
            'id': message.id,
            'user': message.autor,
            'content': message.content,
            'timestamp': str(message.timestamp)
        }


    #sending mesages to chat
    def send_chat_message(self, message):
        self.send(text_data=json.dumps(message))





    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name,
        )

        await self.accept()


        await self.fetch_messages(self,)


    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data):
        #print(text_data)
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        user = text_data_json['user']

        # Send message to room
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'user': user,
                'conecting_user':'',
                'is_history': '',
            }
        )
        message = Message.objects.create(
            autor=User.objects.get(username=text_data_json['user']),
            content=text_data_json['message'])

    # Receive message from room group
    async def chat_message(self, event):
        message = event['message']
        user = event['user']



        # Send message to WebSocket

        cun_user = event['conecting_user']
        is_hist = event['is_history']
        await self.send(text_data=json.dumps({
            'message': message,
            'user': user,
            'conecting_user': str(cun_user),
            'is_history': is_hist,
        }))



