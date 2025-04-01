from rest_framework.response import Response
from rest_framework import status
from utils.views import BaseAPIView
from base.models import Report , Organization
from base.serializers import ReportSerializer , OrganizationReportsSerializer
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


class ReportOrganizationsView(BaseAPIView, generics.ListAPIView):
    serializer_class = OrganizationReportsSerializer
    queryset = Organization.objects.all()
    pagination_class = CustomPagination

    def get_queryset(self):
        queryset = super().get_queryset()
        name = self.request.query_params.get('name')
        if name:   
            queryset = queryset.filter(name__icontains=name)
        return queryset
    
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context

