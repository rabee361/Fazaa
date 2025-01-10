from rest_framework.response import Response
from rest_framework import status
from utils.views import BaseAPIView
from base.models import Report
from base.serializers import ReportSerializer
from rest_framework import generics
from users.models import User
from utils.pagination import CustomPagination


class CreateReportView(BaseAPIView , generics.CreateAPIView):
    serializer_class = ReportSerializer
    queryset = Report.objects.all()


class ReportListView(BaseAPIView, generics.ListAPIView):
    pagination_class = CustomPagination
    serializer_class = ReportSerializer

    def get_queryset(self):
        user = User.objects.get(id=self.kwargs['user_id'])
        return Report.objects.filter(client=user.id)
