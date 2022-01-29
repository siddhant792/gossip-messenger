from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
import json

from apps.chats import (
    models as chats_models,
    utils as chats_utils,
)
from apps.accounts import models as account_models


class ChatsConsumer(WebsocketConsumer):
    """
    Cunsumer class to manage realtime chat
    """

    def connect(self):
        self.user = chats_utils.autheticate_socket_user(dict(self.scope['headers']))
        if not self.user:
            self.close()
        self.room_name = 'open_server'
        self.room_group_name = 'chat_%s' % self.room_name

        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        target_user = text_data_json['target']
        content = text_data_json['content']

        receiver = account_models.User.objects.filter(mobile_number=target_user).first()
        if not receiver:
            return
            
        # save message to db
        chats_models.Message.objects.create(
            sender=self.user,
            receiver=receiver,
            content=content
        )

        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'content': content,
                'target': target_user,
            }
        )

    # Receive message from room group
    def chat_message(self, event):
        content = event['content']
        target_user = event['target']
        
        # Broadcast message
        if self.user.mobile_number == target_user:
            self.send(text_data=json.dumps({
                'content': content,
            }))
