from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from ..serializers import *
from ..models import *
from fcm_django.models import FCMDevice
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework import status
from rest_framework.permissions import AllowAny , IsAuthenticated
from utils.permissions import *
from rest_framework_simplejwt.tokens import RefreshToken
from utils.helper import generate_code
from django.shortcuts import get_object_or_404
from django.db import transaction
from .common import BaseAPIView
# Create your views here.



class ClientSignUpView(APIView):

    @transaction.atomic
    def post(self,request):
        serializer = SignUpUserSerializer(data = request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            data = serializer.data
            user.user_type = 'client'
            user.save()
            token = RefreshToken.for_user(user)
            data['tokens'] = {'refresh':str(token), 'access':str(token.access_token)}
            # send FCM token to the user
            # send it to client over sms
            return Response(data, status=status.HTTP_200_OK)
        else:
            return Response({'error': serializer.errors.values()}, status=status.HTTP_400_BAD_REQUEST)
