from users.models import User , Client , Shareek
from django.db.models import Q
from users.models import UserType
from fcm_django.models import FCMDevice
from firebase_admin.messaging import Message, Notification


def send_client_notification():
    users = User.objects.filter(Q(is_active=True) & Q(user_type=UserType.CLIENT))
    for user in users:
        devices = FCMDevice.objects.filter(user=user)
        for device in devices:
            device.send_message(Message(
                notification=Notification(
                    title="Test Notification",
                    body="This is a test notification"
                )
            ))


def send_shareek_notification():
    users = User.objects.filter(Q(is_active=True) & Q(user_type=UserType.SHAREEK))
    for user in users:
        devices = FCMDevice.objects.filter(user=user)
        for device in devices:
            device.send_message(Message(
                notification=Notification(
                    title="Test Notification",
                    body="This is a test notification"
                )
            ))


def send_all_notification():
    users = User.objects.filter(Q(is_active=True))
    for user in users:
        devices = FCMDevice.objects.filter(user=user)
        for device in devices:
            device.send_message(Message(
                notification=Notification(
                    title="Test Notification",
                    body="This is a test notification"
                )
            ))

