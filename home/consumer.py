from channels.generic.websocket import AsyncWebsocketConsumer


class TableData(AsyncWebsocketConsumer):

    async def connect(self):
        self.group_name = 'tableData'
        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        pass

    async def receive(self, text_data):
        await self.channel_layer.group_send(
            self.group_name,
            {
                'type': 'update_frontend',
                'value': text_data,
            }
        )

    async def update_frontend(self, event):
        print(event['value'])
        await self.send(event['value'])
