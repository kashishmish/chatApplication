# chat/consumers.py
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async
from .models import Messages, OnlineOffline, Personal, PersonalMessage
from django.core import serializers

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.user_name = self.scope['url_route']['kwargs']['user_name']
        self.room_group_name = 'chat_%s' % self.room_name
        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.save_status(self.user_name,"connected")

        await self.accept()


    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
        await self.save_status(self.user_name,"disconnected")

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']


        time=await self.save_message(self.user_name,self.room_name,message)
        time=str(time)
        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'user_name':self.user_name,
                'message': message,
                'time':time,
            }
        )

    # Receive message from room group
    async def chat_message(self, event):
        username = event['user_name']
        message = event['message']
        time=event['time']
        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'user_name':username,
            'message': message,
            'time':time,
        }))
    
    @sync_to_async
    def save_message(self,username,room,message):
        mes=Messages.objects.create(username=username,room_id=room,message=message)
        return mes.datetime
    @sync_to_async
    def save_status(self,username,status):
        stat=OnlineOffline.objects.get(user=username)
        stat.status=status
        stat.save()

class PersonalConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.me = self.scope['url_route']['kwargs']['me']
        self.you = self.scope['url_route']['kwargs']['you']
        chat_id=await self.get_id(self.me,self.you)
        self.room_group_name = 'personalchat_%d' % chat_id
        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.save_status(self.me,"connected")
        await self.accept()

    async def disconnect(self, close_code):
        self.me = self.scope['url_route']['kwargs']['me']
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
        await self.save_status(self.me,"disconnected")

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        me = text_data_json['me']
        you = text_data_json['you']

        chat_id=await self.get_id(me,you)
        chat_time=await self.save_personal_message(chat_id,me,message)
        chat_time=str(chat_time)


        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'me':me,
                'you':you,
                'message': message,
                'time':chat_time,
            }
        )

    # Receive message from room group
    async def chat_message(self, event):
        print(event)
        me = event['me']
        you=event['you']
        message = event['message']
        time=event['time']
        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'me':me,
            'you':you,
            'message': message,
            'time':time,
        }))
    @sync_to_async
    def get_id(self,me,you):
        try:
            id=Personal.objects.get(me=me,user=you)
        except:
            id=Personal.objects.get(me=you,user=me)
        return(id.id)
    @sync_to_async
    def save_personal_message(self,person_id,me,messages):
        personal=PersonalMessage.objects.create(people_id=person_id,sender=me,messages=messages)
        return personal.datetime
    @sync_to_async
    def save_status(self,username,status):
        stat=OnlineOffline.objects.get(user=username)
        stat.status=status
        stat.save()
class LoginStatus(AsyncWebsocketConsumer):
    async def connect(self):
        self.username = self.scope['url_route']['kwargs']['username']
        self.room_group_name = 'connected'
        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()
        await self.save_status(self.username,"connected")
        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message_disconnect',
                'username':self.username,
                'status':"connected"
            }
        )
    async def disconnect(self, close_code):
        self.username = self.scope['url_route']['kwargs']['username']
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

        await self.save_status(self.username,"disconnected")
        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message_disconnect',
            }
        )

    async def chat_message_disconnect(self, event):
        stapeople=await self.show_status(self.username)
        # Send message to WebSocket
        await self.send(text_data=stapeople)
    
    # Receive message from room group
    async def chat_message(self, event):
        # Send message to WebSocket
        await self.send(text_data="hello")
    @sync_to_async
    def save_status(self,username,status):
        stat=OnlineOffline.objects.get(user=username)
        stat.status=status
        stat.save()
    @sync_to_async
    def show_status(self,user):
        stapeople=OnlineOffline.objects.all()
        stapeople1=serializers.serialize('json', stapeople)
        return stapeople1