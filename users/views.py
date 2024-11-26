from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from .serializers import *
from .models import *
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
# Create your views here.





class BaseAPIView(APIView):
    permission_classes = [IsAuthenticated]



class ClientSignUpView(BaseAPIView):

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


class ShareekSignUpView(BaseAPIView):

    @transaction.atomic
    def post(self,request):
        serializer = SignUpUserSerializer(data = request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            data = serializer.data
            user.user_type = 'shareek'
            user.save()
            token = RefreshToken.for_user(user)
            data['tokens'] = {'refresh':str(token), 'access':str(token.access_token)}
            # send FCM token to the user
            # send it to client over sms
            return Response(data, status=status.HTTP_200_OK)
        else:
            return Response({'error': serializer.errors.values()}, status=status.HTTP_400_BAD_REQUEST)




class ShareekRegisterView(BaseAPIView):
    # permission_classes = [IsShareek]

    @transaction.atomic
    def post(self , request):
        serializer = ShareekRegisterSerializer(data = request.data)
        if serializer.is_valid(raise_exception=True):
            data = serializer.save()
            organization = Shareek.create_organization(**data)
            shareek ,created = Shareek.objects.get_or_create(
                user = request.user,
                organization = organization,
                job = data.job
            )
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({'error': serializer.errors.values()}, status=status.HTTP_400_BAD_REQUEST)




class LoginView(BaseAPIView):
    def post(self, request):

        # validate the data
        serializer = LoginSerializer(data = request.data , context={'request':request})
        if serializer.is_valid(raise_exception=True):
            user = serializer.data.get('user')
            token = RefreshToken.for_user(user)
            # set the device token for notification
            device_token = request.data.get('device_token',None)
            device_type = request.data.get('device_type','android')

            data = serializer.data
            data['tokens'] = {'refresh':str(token), 'access':str(token.access_token)}

            return Response(data, status=status.HTTP_200_OK)
        else:
            return Response({'error': serializer.errors.values()}, status=status.HTTP_400_BAD_REQUEST)    


class LogoutView(BaseAPIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        try:
            refresh_token = request.data["refresh_token"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({"message": ["تم تسجيل الخروج بنجاح"]}, status=status.HTTP_200_OK)
        except Exception:
            return Response({"error": ["التوكين غير صحيح"]}, status=status.HTTP_400_BAD_REQUEST)



class ForgetPasswordOTPView(BaseAPIView):
    def post(self,request):
        phonenumber = self.request.data.get('phonenumber',None)
        if phonenumber:
            if OTPCode.checkLimit(phonenumber):
                otp_code = OTPCode.objects.create(phonenumber=phonenumber , code_type='FORGET_PASSWORD')
                #send the code to the user over sms
                #send_code()
                return Response({'message':['تم ارسال رمز التحقق']} , status=status.HTTP_200_OK)
            else:
                return Response({'message':['لقد تجاوزت الحد المسموح لإرسال رمز التفعيل الرجاء المحاولة بعد قليل']} , status=status.HTTP_400_BAD_REQUEST)

        else:
            raise serializers.ValidationError({'error':['أدخل رقم هاتف صحيح']} , status=status.HTTP_400_BAD_REQUEST)
        



class ResetPasswordOTPView(BaseAPIView):
    def post(self,request):
        phonenumber = self.request.data.get('phonenumber',None)
        if phonenumber:
            if OTPCode.checkLimit(phonenumber):
                otp_code = OTPCode.objects.create(phonenumber=phonenumber , code_type='RESET_PASSWORD')
                #send the code to the user over sms
                #send_code()
                return Response({'message':['تم ارسال رمز التحقق']} , status=status.HTTP_200_OK)
            else:
                return Response({'error':['لقد تجاوزت الحد المسموح لإرسال رمز التفعيل الرجاء المحاولة بعد قليل']} , status=status.HTTP_400_BAD_REQUEST)
        else:
            raise serializers.ValidationError({'error':['أدخل رقم هاتف صحيح']} , status=status.HTTP_400_BAD_REQUEST)



class OTPVerificationView(BaseAPIView):
    def post(self,request):
        code = self.request.data.get('code',None)
        if code:
            otp_code = OTPCode.objects.get(code=code)
            if otp_code and otp_code.createdAt >= timezone.localtime() - timezone.timedelta(minutes=15):
                otp_code.is_used = True
                otp_code.save()
                return Response({'message':['تم التحقق بنجاح']} , status=status.HTTP_200_OK)
            else:
                return Response({'error':['رمز التحقق غير موجود أو منتهي الصلاحية']}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'error':['أدخل رمز التحقق']}, status=status.HTTP_400_BAD_REQUEST)



class ResetPasswordView(BaseAPIView):
    def post(self,request):
        ResetPasswordSerializer(request.data).is_valid(raise_exception=True)
        password = request.data.get('password')
        if request.user.check_password(password):
            return Response({"error":["كلمة المرور غير صحيحة"]})
        
        user = request.user
        user.set_password(password)
        user.save()
        return Response({"message":["تم تغيير كلمة السر بنجاح"]} , status=status.HTTP_200_OK)




class NotificationsView(generics.ListAPIView,BaseAPIView):
    serializer_class = NotificationSerializer
    queryset = Notification.objects.all()

    def get_queryset(self,request):
        user = request.user
        return Notification.objects.filter(user=user)




