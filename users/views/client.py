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
from utils.views import BaseAPIView
# Create your views here.



class ClientSignUpView(APIView):

    @transaction.atomic
    def post(self,request):
        serializer = SignUpClientSerializer(data = request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            user.create_signup_otp()
            user.create_chat()
            data = serializer.data
            token = RefreshToken.for_user(user)
            data['tokens'] = {'refresh':str(token), 'access':str(token.access_token)}
            # send FCM token to the user
            # send it to client over sms
            return Response(data, status=status.HTTP_200_OK)
        else:
            return Response({'error': serializer.errors.values()}, status=status.HTTP_400_BAD_REQUEST)



class UpdateClientView(BaseAPIView):
    @transaction.atomic
    def put(self,request,pk):
        user = get_object_or_404(User,pk=pk)
        serializer = UpdateClientSerializer(user,data=request.data,context={'request':request})
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data,status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)



class DeleteClientView(BaseAPIView):
    @transaction.atomic
    def delete(self,request):
        user = request.user
        client = Client.objects.get(user=user)
        client.delete()
        user.delete()
        return Response({'message':'تم حذف الحساب بنجاح'},status=status.HTTP_200_OK)


