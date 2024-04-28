# consumers.py
from channels.generic.websocket import AsyncWebsocketConsumer
import json


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Assuming the user ID is passed via URL
        self.user_id = self.scope['url_route']['kwargs']['user_id']
        self.group_name =  self.user_id

        # Join room group
        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )

        await self.accept()
        # await self.send(json.dumps({"mess": 'Connected'}))

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data):
        # text_data_json = json.loads(text_data)
        # message = text_data_json['message']

        # Send message to room group
        await self.channel_layer.group_send(
            self.group_name,
            {
                'type': 'user_message',
                'message': "message"
            }
        )

        # await self.send(text_data=json.dumps({
        #     'message': message
        # }))
    # Receive message from room group

    async def user_message(self, event):
        data = event['data']

        # Send message to WebSocket
        await self.send(
            json.dumps(data)
        )
