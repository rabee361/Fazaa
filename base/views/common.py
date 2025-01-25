from rest_framework.response import Response
from rest_framework import status
from base.models import TermsPrivacy , CommonQuestion , ContactUs
from base.serializers import TermsPrivacySerializer , CommonQuestionsSerializer , ContactUsSerializer
from utils.views import BaseAPIView



class TermsPrivacyView(BaseAPIView):
    def get(self,request):
        terms = TermsPrivacy.objects.all()
        serializer = TermsPrivacySerializer(terms , many=True)
        return Response(serializer.data , status=status.HTTP_200_OK)



class CommonQuestionsView(BaseAPIView):
    def get(self,request):
        questions = CommonQuestion.objects.all()
        serializer = CommonQuestionsSerializer(questions , many=True)
        return Response(serializer.data , status=status.HTTP_200_OK)


class ContactUsView(BaseAPIView):
    def get(self,request):
        contact_us = ContactUs.objects.all()
        serializer = ContactUsSerializer(contact_us , many=True, context={'request':request})
        return Response(serializer.data , status=status.HTTP_200_OK)
