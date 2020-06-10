from django.views import View
from django.http import HttpResponse

class ConfirmView(View):
    def post(self, request, token):
        return HttpResponse('')


class RejectView(View):pass
