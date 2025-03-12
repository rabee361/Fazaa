from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from ..serializers import *
from ..models import *
from fcm_django.models import FCMDevice
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from utils.permissions import *
from rest_framework import generics
from rest_framework_simplejwt.tokens import RefreshToken
from utils.views import BaseAPIView
from utils.pagination import CustomPagination






class RefreshTokenView(BaseAPIView):
    def post(self,request):
        refresh = request.data.get('refresh')
        if not refresh:
            return Response({"error":"الرجاء إدخال التوكين"},status=status.HTTP_400_BAD_REQUEST)
        try:
            token = RefreshToken(refresh)
            return Response({"access":str(token.access_token)},status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error":"حدث خطأ ما"},status=status.HTTP_401_UNAUTHORIZED)


class RefreshFirebaseToken(BaseAPIView):

    def post(self,request):
        token = request.data['firebase-token']
        user_id = request.data['user_id']
        try:
            user = User.objects.get(id=user_id)
            device = FCMDevice.objects.get(user=user)
            device.registration_id = token
            device.save()
        except User.DoesNotExist:
            return ErrorResult("المستخدم غير موجود",status=404)

        return Response({
            "msg" : "firebase token changed successfully"
        },status=status.HTTP_200_OK)



class LoginView(APIView):
    def post(self, request):
        # validate the data
        if not 'phonenumber' in request.data:
            return Response({'error':'الرجاء إدخال رقم الهاتف'}, status=status.HTTP_400_BAD_REQUEST)
        if not 'password' in request.data:
            return Response({'error': 'الرجاء إدخال كلمة السر'}, status=status.HTTP_400_BAD_REQUEST)
        phonenumber = request.data.get('phonenumber')
        password = request.data.get('password')
        user=authenticate(request,phonenumber=phonenumber,password=password)
        if user:
            # set the device token for notification 
            device_token = request.data.get('device_token',None)
            device_type = request.data.get('device_type','android')
            try:
                device_tok = FCMDevice.objects.get(registration_id=device_token ,type=device_type)
                device_tok.user = user
                device_tok.save()
            except:
                if device_token and device_token != '':
                    FCMDevice.objects.create(user=user , registration_id=device_token ,type='android')
                else:
                    pass
            token = RefreshToken.for_user(user)
            data = {
                **UserSerializer(instance=user, context={'request': request}).data,
                'refresh':str(token),
                'access':str(token.access_token),
            }
            return Response(data, status=status.HTTP_200_OK)
        else:
            return Response({'error':'خطأ في رقم الهاتف أو كلمة المرور'}, status=status.HTTP_400_BAD_REQUEST)


class LogoutView(BaseAPIView):
    def post(self, request):
        try:
            if 'refresh' not in request.data:
                refresh_token = request.data["refresh"]
                token = RefreshToken(refresh_token)
                token.blacklist()
                return Response({"message": "تم تسجيل الخروج بنجاح"}, status=status.HTTP_200_OK)
            else:
                return Response({"error": "الرجاء إدخال التوكين"}, status=status.HTTP_400_BAD_REQUEST)

        except Exception:
            return Response({"error": "التوكين غير صحيح"}, status=status.HTTP_400_BAD_REQUEST)



class SignUpOTPView(BaseAPIView):
    def post(self,request):
        phonenumber = self.request.data.get('phonenumber',None)
        if phonenumber is None:
            return Response({"error":'الرجاء إدخال رقم الهاتف'})
        if not OTPCode.checkLimit(phonenumber):
            otp_code = OTPCode.objects.create(phonenumber=phonenumber , code_type=CodeTypes.SIGNUP)
            #send the code to the user over whatsapp
            #send_code()
            return Response({'message':'تم ارسال رمز التحقق'} , status=status.HTTP_200_OK)
        else:
            return Response({'error':'لقد تجاوزت الحد المسموح لإرسال رمز التفعيل الرجاء المحاولة بعد قليل'} , status=status.HTTP_400_BAD_REQUEST)




class ForgetPasswordOTPView(BaseAPIView):
    def post(self,request):
        phonenumber = self.request.data.get('phonenumber',None)
        if phonenumber:
            if not OTPCode.checkLimit(phonenumber):
                otp_code = OTPCode.objects.create(phonenumber=phonenumber , code_type=CodeTypes.FORGET_PASSWORD)
                #send the code to the user over sms
                #send_code()
                return Response({'message':'تم ارسال رمز التحقق'} , status=status.HTTP_200_OK)
            else:
                return Response({'error':'لقد تجاوزت الحد المسموح لإرسال رمز التفعيل الرجاء المحاولة بعد قليل'} , status=status.HTTP_400_BAD_REQUEST)
        else:
            raise serializers.ValidationError({'error':'أدخل رقم هاتف صحيح'} , status=status.HTTP_400_BAD_REQUEST)





class ResetPasswordOTPView(BaseAPIView):
    def post(self,request):
        phonenumber = self.request.data.get('phonenumber',None)
        if phonenumber:
            if not OTPCode.checkLimit(phonenumber):
                otp_code = OTPCode.objects.create(phonenumber=phonenumber , code_type=CodeTypes.RESET_PASSWORD)
                #send the code to the user over sms
                #send_code()
                return Response({'message':'تم ارسال رمز التحقق'} , status=status.HTTP_200_OK)
            else:
                return Response({'error':'لقد تجاوزت الحد المسموح لإرسال رمز التفعيل الرجاء المحاولة بعد قليل'} , status=status.HTTP_400_BAD_REQUEST)
        else:
            raise serializers.ValidationError({'error':'أدخل رقم هاتف صحيح'} , status=status.HTTP_400_BAD_REQUEST)



class OTPVerificationView(APIView):
    def post(self,request):
        code = self.request.data.get('code',None)
        if code: 
            try:
                otp_code = OTPCode.objects.get(code=code)
                try:
                    user = User.objects.get(phonenumber=otp_code.phonenumber)
                except User.DoesNotExist:
                    user = None
                if otp_code and otp_code.createdAt >= timezone.localtime() - timezone.timedelta(minutes=15):
                    with transaction.atomic():
                        otp_code.is_used = True
                        otp_code.save()
                    return Response({'message':'تم التحقق بنجاح', 'user_id':user.id} , status=status.HTTP_200_OK)
                else:
                    return Response({'error':'رمز التحقق منتهي الصلاحية'} , status=status.HTTP_400_BAD_REQUEST)
            except OTPCode.DoesNotExist:
                return Response({'error':'رمز التحقق غير موجود'} , status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'error':'أدخل رمز التحقق'} , status=status.HTTP_400_BAD_REQUEST)



class ChangePasswordView(BaseAPIView):
    def post(self,request):
        password = request.data.get('password')
        new_password = request.data.get('new_password')
        ChangePasswordSerializer(data=request.data).is_valid(raise_exception=True)
        if request.user.check_password(password):
            user = request.user
            user.set_password(new_password)
            user.save()
            return Response({"message":'تم تغيير كلمة السر بنجاح'} , status=status.HTTP_200_OK)
        else:
            return Response({"error":'كلمة المرور غير صحيحة'}, status=status.HTTP_400_BAD_REQUEST)


class ResetPasswordView(APIView):
    def post(self,request,user_id):
        ResetPasswordSerializer(data=request.data).is_valid(raise_exception=True)
        user = User.objects.get(id=user_id)
        user.set_password(request.data.get('new_password'))
        user.save()
        return Response({"message":'تم تغيير كلمة السر بنجاح'} , status=status.HTTP_200_OK)



class NotificationsView(generics.ListAPIView,BaseAPIView):
    serializer_class = UserNotificationSerializer
    pagination_class = CustomPagination

    def get_queryset(self):
        user = self.request.user
        notifications = UserNotification.objects.filter(user=user)
        return notifications



class ActivateNotificationsView(APIView):
    def post(self,request,user_id):
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({"error":'المستخدم غير موجود'} , status=status.HTTP_404_NOT_FOUND)
        
        get_notifications = request.data.get('get_notifications','deactivate')
        if get_notifications == 'activate':
            user.get_notifications = True
        elif get_notifications == 'deactivate':
            user.get_notifications = False
        else:
            return Response({"error":'الرجاء إدخال قيمة صحيحة'} , status=status.HTTP_400_BAD_REQUEST)
        user.save()
        return Response({"message":'تم تحديث الإعدادات بنجاح'} , status=status.HTTP_200_OK)




class UpdateLocationView(BaseAPIView):
    def post(self,request,user_id):
        user = User.objects.get(id=user_id)
        new_long = request.data.get('long',None)
        new_lat = request.data.get('lat',None)
        if new_long and new_lat:
            user.long = new_long
            user.lat = new_lat
            user.save()
            return Response({"message":'تم تحديث الموقع بنجاح'} , status=status.HTTP_200_OK)
        else:
            return Response({"error":'الرجاء إدخال الموقع'} , status=status.HTTP_400_BAD_REQUEST)




class DeleteAccountView(APIView):
    def delete(self,request,user_id):
        user = User.objects.get(id=user_id)
        user.delete()
        return Response({"message":"تم حذف الحساب بنجاح"} , status=status.HTTP_204_NO_CONTENT)