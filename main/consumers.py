import json
from channels.generic.websocket import AsyncWebsocketConsumer
import random
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync, sync_to_async
from datetime import datetime
from .models import Message
from .models import User



class ChatConsumer(AsyncWebsocketConsumer):
    rooms = {}
    async def connect(self):
       
        available_rooms = [room_name for room_name, users in self.rooms.items() if len(users) == 1]


        if available_rooms:
            self.room_group_name = random.choice(available_rooms)
        else:
           
            self.room_group_name = f"chat_{random.randint(1000, 9999)}"
            self.rooms[self.room_group_name] = set()

        self.rooms[self.room_group_name].add(self.channel_name)

        await (self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name

        )
        await self.accept()

    async def end_chat(self):
        # Oda grubuna "sohbet sona erdi" mesajını gönderin
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'end_chat_message',
                'message': 'Chat end.'
            }
        )

    async def disconnect(self, close_code):

        
        # Remove current user from the room
        self.rooms[self.room_group_name].discard(self.channel_name)

        # If room becomes empty, remove it
        #if not self.rooms[self.room_group_name]:
        #    del self.rooms[self.room_group_name]

        # Leave room group
        await(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )
        await self.end_chat()

   
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]
        sender_username = self.scope["user"].username
        #receiver_username = text_data_json['receiver_username'] 

        await(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type':'chat_message',
                'message':message,
                'sender_username': sender_username,
                #'receiver_user': receiver_username,
            }
        )

    async def chat_message(self,event):
        message = event['message']
        sender_username = event['sender_username']

        await self.send(text_data=json.dumps({
                'type':'chat',
                'message':message,
                'sender_username': sender_username,

        }))

    async def end_chat_message(self, event):
        message = event['message']
        # Kullanıcıya sohbet sona erdi mesajını gönderin
        await self.send(text_data=json.dumps({
            'type': 'end_chat',
            'message': message
        }))

from django.db.models import Q


class PrivateChatConsumer(WebsocketConsumer):
    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f'chat_{self.room_name}'
        user= self.scope["user"]

        # Kullanıcıyı odanın grubuna katılması için sendiri ekler
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        self.accept()

        messages = Message.objects.filter(
            Q(sender=user) | Q(receiver=user)
        ).order_by('timestamp')[:20]

        last_messages = [{
            'sender_username': message.sender.username,
            'message': message.content,
            'timestamp': message.timestamp.strftime("%H:%M"),
        } for message in messages]

        self.send(text_data=json.dumps({
            'last_messages': last_messages
        })) 

    def disconnect(self, close_code):
        # Kullanıcıyı odanın grubundan çıkarır
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )
    def receive(self, text_data=None, bytes_data=None):
        if text_data:
            text_data_json = json.loads(text_data)
            message_content = text_data_json['message']
            sender_username = self.scope["user"].username
            receiver_username = text_data_json['receiver_username'] 
            receiver_user = User.objects.get(username=receiver_username)
            timestamp = datetime.now().strftime("%H:%M")


            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'message': message_content,
                    'sender_username': sender_username,
                    'receiver_user': receiver_username,
                    'timestamp': timestamp,
                }
            )
            
            message = Message.objects.create(
            sender = self.scope["user"],
            receiver = receiver_user,
            content = message_content,
            timestamp = timestamp,
            )
            message.save()
        
        elif bytes_data:
            
            print("Received audio data")

            # Ses verisini bir dosyaya kaydet
            audio_filename = f"{self.scope['user'].username}_{datetime.now().strftime('%Y%m%d%H%M%S')}.mp3"
            with open(audio_filename, "wb") as audio_file:
                audio_file.write(bytes_data)

            # Ses verisini gruba yayınla
            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name,
                {
                    'type': 'audio_message',
                    'sender_username': self.scope['user'].username,
                    'audio_filename': audio_filename,
                }
            )


    # Gruba gönderilen mesajları alır/bize gelen mesajlar
    def chat_message(self, event):
        message_content = event['message']
        sender_username = event['sender_username']
        receiver_user = event['receiver_user']
        timestamp = datetime.now().strftime("%H:%M")
        
        
        # Alınan mesajı WebSocket bağlantısına gönderir
        self.send(text_data=json.dumps({
            'type': 'chat_message',
            'message': message_content,
            'sender_username': sender_username,
            'timestamp': timestamp,
            
        }))

    def audio_message(self, event):
        sender_username = event['sender_username']
        audio_filename = event['audio_filename']

        # Alınan ses verisini istemciye gönder
        with open(audio_filename, "rb") as audio_file:
            audio_data = audio_file.read()
            self.send(bytes_data=audio_data)





