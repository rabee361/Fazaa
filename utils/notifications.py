from users.models import User
from django.db.models import Q
from users.models import UserType
from fcm_django.models import FCMDevice
from firebase_admin.messaging import Message, Notification , UnregisteredError
from firebase_admin.exceptions import InvalidArgumentError
from users.models import UserNotification

def send_users_notification(title,body,recipient_type):
    if recipient_type == 'all':
        users = User.objects.filter(Q(is_active=True))
    elif recipient_type == 'clients':
        users = User.objects.filter(Q(is_active=True) & Q(user_type=UserType.CLIENT))
    elif recipient_type == 'shareeks':
        users = User.objects.filter(Q(is_active=True) & Q(user_type=UserType.SHAREEK))

    for user in users:
        devices = FCMDevice.objects.filter(user=user)
        for device in devices:
            try:
                device.send_message(Message(
                    notification=Notification(
                        title=title,
                        body=body
                    )
                ))
            except UnregisteredError as e:
                pass
            except InvalidArgumentError as e:
                pass
        
        notification = UserNotification.objects.create(
            user=user,
            title=title,
            content=body
        )
