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
from utils.permissions import IsShareekUser , IsClientUser
# Create your views here.



class ShareekSignUpView(APIView):

    @transaction.atomic
    def post(self,request):
        serializer = SignUpShareekSerializer(data = request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            code = user.create_signup_otp()
            chat_id = user.create_chat()
            data = serializer.data
            token = RefreshToken.for_user(user)
            data['tokens'] = {'refresh':str(token), 'access':str(token.access_token)}
            data['code'] = code
            data['chat_id'] = chat_id
            # send FCM token to the user
            # send it to client over sms
            return Response(data, status=status.HTTP_200_OK)
        else:
            return Response({'error': serializer.errors.values()}, status=status.HTTP_400_BAD_REQUEST)




class ShareekRegisterView(BaseAPIView):

    def post(self, request):
        ShareekRegisterSerializer(data=request.data).is_valid(raise_exception=True)
        image = request.data.get('image', None)
        user = request.user
        user.email = request.data.get('email', None)
        user.full_name = request.data.get('full_name', None)
        if image:
            user.image = image
        user.user_type = 'SHAREEK'
        user.save()
        
        # Check if the organization already exists or create a new one
        organization = Shareek.create_organization(**request.data)
        
        # Check if a Shareek instance already exists for this user
        shareek = Shareek.objects.filter(user=user).first()
        
        if not shareek:
            # If no existing Shareek, create a new one
            shareek = Shareek.objects.create(
                user=user,
                job=request.data.get('job', None),
                organization=organization
            )
            return Response({
                **UserSerializer(instance=shareek.user, context={'request':request}).data,
                'job': shareek.job,
                'organization_name': organization.name,
                'organization_type': organization.organization_type.name,
                'commercial_register_id': organization.commercial_register_id,
            }, status=status.HTTP_201_CREATED)
        else:
            # If Shareek already exists, return an error response
            return Response({"error": "يوجد شريك مسجل بهذا الرقم "}, status=status.HTTP_400_BAD_REQUEST)



class ShareekInfoView(BaseAPIView):
    def get(self,request,id):
        try:
            shareek = Shareek.objects.select_related('organization','user').get(user__id=id)
            user = shareek.user
            organization = shareek.organization
            return Response({
                **ShareekSerializer(instance=shareek).data,
                **UserSerializer(instance=user, context={'request':request}).data,
                'organization_name': organization.name,
                'organization_type': organization.organization_type.name,
                'organization_type_id': organization.organization_type.id,
                'commercial_register_id': organization.commercial_register_id,
            },status=status.HTTP_200_OK)
        except Shareek.DoesNotExist:
            raise ErrorResult({"error":"لا يوجد شريك مسجل بهذه المعلومات"} ,status=404)


class UpdateShareekView(BaseAPIView):
    @transaction.atomic
    def put(self ,request,pk):
        try:
            user = User.objects.get(id=pk, is_deleted=False)
            serializer = UpdateShareekSerializer(user,data=request.data , context={'request':request})
            if serializer.is_valid(raise_exception=True):
                user = serializer.save()
                shareek = Shareek.objects.get(user=user)
                return Response({
                    **serializer.data,
                    'job': shareek.job,
                    'organization_name': shareek.organization.name,
                    'organization_type_id': shareek.organization.organization_type.id,
                    'commercial_register_id': shareek.organization.commercial_register_id,
                },status=status.HTTP_200_OK)
            else:
                return ErrorResult(serializer.errors,status=400)
        except User.DoesNotExist:
            raise ErrorResult("لا يوجد شريك مسجل بهذه المعلومات" ,status=404)


class DeleteShareekView(BaseAPIView):
    @transaction.atomic
    def delete(self,request):
        try:
            user = request.user
            user.is_deleted = True
            shareek = Shareek.objects.get(user=user)
            shareek.organization.delete()
            user.save()
            shareek.save()
            return Response({'message':'تم حذف الحساب بنجاح'},status=status.HTTP_200_OK)
        except User.DoesNotExist:
            raise ErrorResult("لا يوجد شريك مسجل بهذه المعلومات" ,status=404)