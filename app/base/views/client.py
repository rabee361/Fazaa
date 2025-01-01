from rest_framework.response import Response
from rest_framework import status
from utils.views import BaseAPIView
from app.base.models import Report
from app.base.serializers import ReportSerializer
from rest_framework import generics


class CreateReportView(BaseAPIView , generics.CreateAPIView):
    serializer_class = ReportSerializer
    queryset = Report.objects.all()


class ReportListView(BaseAPIView , generics.ListAPIView):
    serializer_class = ReportSerializer
    queryset = Report.objects.all()


