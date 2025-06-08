import json
from channels.generic.websocket import AsyncWebsocketConsumer

class BookAvailabilityConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        """Connect to the book availability group"""
        await self.channel_layer.group_add(
            'book_availability',
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        """Disconnect from the book availability group"""
        await self.channel_layer.group_discard(
            'book_availability',
            self.channel_name
        )

    async def book_available(self, event):
        """Send book availability notification to WebSocket"""
        await self.send(text_data=json.dumps({
            'type': 'book.available',
            'book_id': event['book_id'],
            'title': event['title'],
            'message': event['message']
        })) 
