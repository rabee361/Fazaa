import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from asgiref.sync import async_to_sync
import json
from users.models import Message, SupportChat, User
from .serializers import MessageSerializer, SupportChatSerializer, UserSerializer
from fcm_django.models import FCMDevice
from firebase_admin.messaging import Message as FCMessage, Notification
from django.core.exceptions import ObjectDoesNotExist



class SendMessage(AsyncWebsocketConsumer):
	async def connect(self):
		try:
			# Debug information
			print("WebSocket connection attempt")
			print(f"Scope: {self.scope}")
			print(f"URL route: {self.scope.get('url_route', {})}")
			
			self.chat_id = self.scope['url_route']['kwargs']['chat_id']
			# Get user from authentication
			self.user = self.scope['user']
			# Debug user information
			print(f"User authenticated: {self.user.is_authenticated}")
			if self.user.is_authenticated:
				print(f"User ID: {self.user.id}, User type: {self.user.user_type}")
			
			# Check if user is authenticated
			if not self.user.is_authenticated:
				print(f"Authentication failed: User is not authenticated")
				await self.close(code=403)  # Authentication failed
				return
				
			self.user_id = self.user.id
			self.room_group_name = str(self.chat_id)
			
			# Verify chat exists
			chat = await self.get_chat(self.chat_id)
			if not chat:
				print(f"Chat with ID {self.chat_id} does not exist")
				await self.close(code=4004)  # Not found
				return

			# Verify permissions
			chat_owner = await self.get_chat_owner(self.chat_id)
			if chat_owner == self.user_id or await self.is_admin(self.user_id):
				print(f"User {self.user_id} connected to chat {self.chat_id}")
				# Add to channel layer group
				await self.channel_layer.group_add(
					self.room_group_name,
					self.channel_name
				)
				await self.accept()
			else:
				print(f"Permission denied: User {self.user_id} is not the owner of chat {self.chat_id}")
				await self.close(code=4003)  # Permission denied
				return

		except Exception as e:
			print(f"Connection error: {str(e)}")
			await self.close(code=4000)  # Generic error

	async def receive(self, text_data):
		try:
			text_data_json = json.loads(text_data)
			message_type = text_data_json.get('type')
			
			if message_type == 'fetch_messages':
				# Handle fetch messages request
				messages = await self.get_chat_msgs(self.chat_id)
				await self.send(text_data=json.dumps({
					'type': 'message_history',
					'messages': messages
				}))
				return
			
			message = text_data_json.get('message')
			if not message:
				return

			# Use the authenticated user directly
			user = self.user
			chat = await self.get_chat(self.chat_id)

			# Save the message
			msg = Message(sender=user, content=message, chat=chat)
			await self.save_message(msg)

			# Format message for sending
			message_data = {
				'type': 'chat_message',
				'message': message,
				'sender': user.id,
				'chat': chat.id,
				'createdAt': msg.createdAt.isoformat() if hasattr(msg, 'createdAt') else None
			}

			# Broadcast message to group
			await self.channel_layer.group_send(
				self.room_group_name,
				message_data
			)

			# Send notification
			await self.send_message_notification(chat, user.full_name, message)

		except Exception as e:
			print(f"Message handling error: {str(e)}")
			await self.send(text_data=json.dumps({
				'error': 'Failed to process message'
			}))

	async def chat_message(self, event):
		# Send message to WebSocket
		await self.send(text_data=json.dumps({
			'type': 'chat_message',
			'message': event['message'],
			'sender': event['sender'],
			'chat': event['chat'],
			'createdAt': event['createdAt']
		}))

	@database_sync_to_async
	def send_message_notification(self,chat,title,body):
		device = FCMDevice.objects.filter(user=chat.user)
		device.send_message(
			message=FCMessage(
				notification=Notification(
					title=title,
					body=body
				),
			),
		)

	@database_sync_to_async
	def get_chat_msgs(self,chat_id):
		messages = Message.objects.filter(chat=chat_id).order_by('createdAt')
		return [
			{
				'message': msg.content,
				'sender': msg.sender.id,
				'chat': msg.chat.id,
				'createdAt': msg.createdAt.isoformat() if hasattr(msg, 'createdAt') else None
			}
			for msg in messages
		]

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
		# Leave room group
		await self.channel_layer.group_discard(
			self.room_group_name,
			self.channel_name
		)



