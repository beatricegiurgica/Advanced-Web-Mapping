import json 
from channels.generic.websocket import AsyncWebsocketConsumer

class CityUpdatesConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        await self.accept()

        await self.send(text_data=json.dumps({
            'type': 'connection',
            'message': 'Connected to Cities API real-time updates'
        }))

    async def disconnect(self, close_code):
        pass