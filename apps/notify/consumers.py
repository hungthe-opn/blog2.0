import json

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer


class NotificationConsumer(WebsocketConsumer):
    def connect(self):
        self.room_name = 'test_consumers'
        self.room_group_name = 'test_consumers_group'
        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )
        self.accept()
        self.send(text_data=json.dumps({'status': 'connected form django ^ ^'}))

    def receive(self, text_data):
        print('text_data:', text_data)
        self.send(text_data=json.dumps({'status': 'websocket ^ ^ ^'}))

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    def send_notification(self, event):
        print(event)
        print(event.get('value'))
        data = json.loads(event.get('value'))
        self.send(text_data=json.dumps({'payload': data}))
