# chat/consumers.py
import json
from channels.generic.websocket import AsyncWebsocketConsumer


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        print(self.room_name)
        self.room_group_name = f"chat_{self.room_name}"
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)

        await self.accept()
        print("Accepted")

        # await self.channel_layer.group_send(
        #     self.room_group_name, {"type": "tester_message", "tester": "tester"}
        # )

    # async def tester_message(self, event):
    #     tester = event["tester"]
    #     await self.send(text_data=json.dumps({"tester": tester}))

    async def chat_message(self, event):
        message = event["message"]
        username = event["username"]
        print("U: ", username)
        await self.send(
            text_data=json.dumps({"message": message, "username": username})
        )

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        print("Message received")
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]
        username = text_data_json["username"]
        print(username)
        print("Message: ", message)
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "chat_message",
                "message": message,
                "username": username,
                "hoy": "hoy",
            },
        )
