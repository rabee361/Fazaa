from users.models import User , Client , Shareek
from django.db.models import Q
from users.models import UserType
from fcm_django.models import FCMDevice
from firebase_admin.messaging import Message, Notification


def send_client_notification(title,body):
    users = User.objects.filter(Q(is_active=True) & Q(user_type=UserType.CLIENT))
    for user in users:
        devices = FCMDevice.objects.filter(user=user)
        for device in devices:
            device.send_message(Message(
                notification=Notification(
                    title=title,
                    body=body
                )
            ))


def send_shareek_notification(title,body):
    users = User.objects.filter(Q(is_active=True) & Q(user_type=UserType.SHAREEK))
    for user in users:
        devices = FCMDevice.objects.filter(user=user)
        for device in devices:
            device.send_message(Message(
                notification=Notification(
                    title=title,
                    body=body
                )
            ))


def send_all_notification(title,body):
    users = User.objects.filter(Q(is_active=True))
    for user in users:
        devices = FCMDevice.objects.filter(user=user)
        for device in devices:
            device.send_message(Message(
                notification=Notification(
                    title=title,
                    body=body
                )
            ))

