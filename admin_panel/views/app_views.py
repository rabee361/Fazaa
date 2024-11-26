from django.views import View , generic
from users.models import *
from base.models import *


class ListReportsView(generic.ListView):
    model = Report

class GetReportView(generic.DeleteView):
    model = Report

class DeleteReportView(generic.DeleteView):
    model = Report



class CommonQuestionsView(generic.ListView):
    model = CommonQuestion

class CreateQuestionView(generic.DeleteView):
    model = CommonQuestion

class UpdateQuestionView(generic.DeleteView):
    model = CommonQuestion

class DeleteQuestionView(generic.DeleteView):
    model = CommonQuestion



class NotificationsView(generic.ListView):
    model = Notification