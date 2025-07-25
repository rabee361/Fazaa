from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.views.generic import ListView
from django.views import View
from utils.permissions import IsClientUser , IsShareekUser
from utils.mixins import CustomLoginRequiredMixin


# for admin panel only 
class CustomListBaseView(CustomLoginRequiredMixin, ListView):
    """Base view that adds specified field verbose names to the context"""
    context_fields = []
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['field_names'] = [
            self.model._meta.get_field(field).verbose_name
            for field in self.context_fields
        ]
        return context


class BaseAPIView(APIView):
    pass
    # permission_classes = [IsAuthenticated, IsShareekUser , IsClientUser]


class BaseView(CustomLoginRequiredMixin, View):
    pass
