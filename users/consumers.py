
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from asgiref.sync import async_to_sync
import json
from users.models import Message , SupportChat, User
from .serializers import MessageSerializer , SupportChatSerializer , UserSerializer
from fcm_django.models import FCMDevice
from firebase_admin.messaging import Message, Notification


class CreateMessage(AsyncWebsocketConsumer):
	async def connect(self):
		self.chat_id = self.scope['url_route']['kwargs']['chat_id']
		self.user_id = self.scope['url_route']['kwargs']['user_id']
		self.room_group_name = str(self.chat_id)
		messages = await self.get_chat_msgs(self.chat_id)

		await self.channel_layer.group_add(
			self.room_group_name,
			self.channel_name
		)

		chat_owner = await self.get_chat_owner(self.chat_id)

		if chat_owner == int(self.user_id) or await self.is_admin(self.user_id):
			await self.accept()
		else:
			raise ValueError('this is not your chat')

		for message in messages:
			await self.send(text_data=json.dumps(message))

	async def receive(self, text_data):
		text_data_json = json.loads(text_data)
		message = text_data_json['message']

		user = await self.get_user(self.user_id)
		chat = await self.get_chat(self.chat_id)

		try:
			await self.get_admin(user.id)
			msg = Message(sender=user,content=message, chat=chat,  sent_user=False)
		except User.DoesNotExist:
			msg = Message(sender=user,content=message, chat=chat,  sent_user=True)


		serializer = MessageSerializer(msg,many=False)
		await self.save_message(msg)

		
		await self.channel_layer.group_send(
			self.room_group_name,
			{
				'type':'chat_message',
				'id' : serializer.data['id'],
				'user' : serializer.data['user'],
				'content': serializer.data['content'],
				'createdAt': serializer.data['createdAt'],
				'sent_user': serializer.data['sent_user'],				
				'chat': serializer.data['chat']				
			}
		)

		await self.send_message_notification(chat,user.full_name,message)


	async def send_chat_message(self, event):
		id = event['id']
		content = event['content']
		createdAt = event['createdAt']
		user = event['user']
		sent_user = event['sent_user']
		chat = event['chat']

		await self.send(text_data=json.dumps({
			'id':id,
			'user': user,
			'content': content,
			'createdAt': createdAt,
			'sent_user': sent_user,
			'chat': chat

		}))



	@database_sync_to_async
	def send_message_notification(self,chat,title,body):
		device = FCMDevice.objects.filter(user=chat.user)
		device.send_message(
			message=Message(
				notification=Notification(
					title=title,
					body=body
				),
			),
		)

	@database_sync_to_async
	def get_device(chat):
		return FCMDevice.objects.filter(user=chat.user)

	@database_sync_to_async
	def get_devices(self,user_ids):
		return FCMDevice.objects.filter(user__in=user_ids).values_list('registration_id', flat=True)

	@database_sync_to_async
	def get_chat_msgs(self,chat_id):
		messages = Message.objects.filter(chat=chat_id).order_by('timestamp')
		serializer = MessageSerializer(messages,many=True)
		return serializer.data

	@database_sync_to_async
	def get_user(self, user_id):
		return User.objects.get(id=user_id)

	@database_sync_to_async
	def get_admin(self, user_id):
		return User.objects.get(id=user_id , user_type='ADMIN')

	@database_sync_to_async
	def get_chat(self, chat_id):
		return SupportChat.objects.get(id=chat_id)

	@database_sync_to_async
	def get_chat_owner(self, chat_id):
		chat = SupportChat.objects.get(id=chat_id)
		return int(chat.user.id)

	@database_sync_to_async
	def is_admin(self, user_id):
		user = User.objects.get(id=user_id)
		return user.user_type == 'ADMIN'

	@database_sync_to_async
	def save_message(self, msg):
		msg.save()

	async def disconnect(self, close_code):
		pass



