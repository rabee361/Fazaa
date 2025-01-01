from rest_framework.response import Response
from rest_framework import status
from app.base.models import TermsPrivacy , CommonQuestion
from app.base.serializers import TermsPrivacySerializer , CommonQuestionsSerializer
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
