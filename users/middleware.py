from urllib.parse import parse_qs
from users.models import User
from channels.auth import AuthMiddlewareStack
from channels.db import database_sync_to_async
from django.conf import settings
from django.contrib.auth.models import AnonymousUser
from django.db import close_old_connections
from jwt import InvalidSignatureError, ExpiredSignatureError, DecodeError
from jwt import decode as jwt_decode
from django.contrib.sessions.models import Session
from django.contrib.auth import get_user_model
import traceback


class JWTAuthMiddleware:
    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, receive, send):
        close_old_connections()
        try:
            # First try session-based authentication
            user = await self.get_user_from_session(scope)
            if not isinstance(user, AnonymousUser):
                scope['user'] = user
                return await self.app(scope, receive, send)

            # If session auth fails, try JWT authentication
            headers = dict(scope.get('headers', []))
            auth_header = headers.get(b'authorization', b'').decode()
            
            if auth_header.startswith('Bearer '):
                jwt_token = auth_header.split(' ')[1]
                jwt_payload = self.get_payload(jwt_token)
                user_credentials = self.get_user_credentials(jwt_payload)
                user = await self.get_logged_in_user(user_credentials)
                scope['user'] = user
            else:
                scope['user'] = AnonymousUser()

        except (InvalidSignatureError, KeyError, ExpiredSignatureError, DecodeError):
            traceback.print_exc()
            scope['user'] = AnonymousUser()
        except Exception as e:
            print(f"Authentication error: {str(e)}")
            traceback.print_exc()
            scope['user'] = AnonymousUser()
        
        return await self.app(scope, receive, send)

    @database_sync_to_async
    def get_user_from_session(self, scope):
        try:
            # Get the session key from cookies
            cookies = parse_qs(scope.get('query_string', b'').decode())
            session_key = None

            # First try to get session from query params
            if 'session_key' in cookies:
                session_key = cookies['session_key'][0]
            else:
                # Try to get session from cookie header
                headers = dict(scope.get('headers', []))
                cookie_header = headers.get(b'cookie', b'').decode()
                if cookie_header:
                    cookies = {
                        cookie.split('=')[0].strip(): cookie.split('=')[1].strip()
                        for cookie in cookie_header.split(';')
                        if '=' in cookie
                    }
                    session_key = cookies.get('sessionid')

            if not session_key:
                return AnonymousUser()

            # Get the session and user
            session = Session.objects.get(session_key=session_key)
            uid = session.get_decoded().get('_auth_user_id')
            
            if not uid:
                return AnonymousUser()

            User = get_user_model()
            user = User.objects.get(id=uid)
            
            # Check if user is staff/admin for admin routes
            if not user.is_staff:
                return AnonymousUser()
            
            return user

        except (Session.DoesNotExist, User.DoesNotExist, KeyError):
            return AnonymousUser()
        except Exception as e:
            print(f"Session authentication error: {str(e)}")
            return AnonymousUser()

    def get_payload(self, jwt_token):
        payload = jwt_decode(
            jwt_token, settings.SECRET_KEY, algorithms=["HS256"])
        return payload

    def get_user_credentials(self, payload):
        """
        method to get user credentials from jwt token payload.
        defaults to user id.
        """
        user_id = payload['user_id']
        return user_id

    async def get_logged_in_user(self, user_id):
        user = await self.get_user(user_id)
        return user

    @database_sync_to_async
    def get_user(self, user_id):
        try:
            return User.objects.get(id=user_id)
        except User.DoesNotExist:
            return AnonymousUser()


def JWTAuthMiddlewareStack(app):
    return JWTAuthMiddleware(AuthMiddlewareStack(app))