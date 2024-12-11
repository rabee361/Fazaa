from django.views import View , generic
from users.models import *
from base.models import *
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator


login_required_m =  method_decorator(login_required, name="dispatch")

class ListReportsView(generic.ListView):
    model = Report
    context_object_name = 'reports'

class GetReportView(generic.DeleteView):
    model = Report
    context_object_name = 'report'

class DeleteReportView(generic.DeleteView):
    model = Report
    context_object_name = 'report'



class CommonQuestionsView(generic.ListView):
    model = CommonQuestion
    context_object_name = 'questions'

class CreateQuestionView(generic.DeleteView):
    model = CommonQuestion
    context_object_name = 'question'

class UpdateQuestionView(generic.DeleteView):
    model = CommonQuestion
    context_object_name = 'question'

class DeleteQuestionView(generic.DeleteView):
    model = CommonQuestion
    context_object_name = 'question'



class BaseNotificationsView(generic.ListView):
    model = Notification


class SendNotificationView(View):
    def post(self,request):
        pass



class AboutUsView(generic.ListView):
    model = AboutUs
    context_object_name = 'about'


class UpdateAboutUsView(generic.UpdateView):
    model = AboutUs
    context_object_name = 'about'