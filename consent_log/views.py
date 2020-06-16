from django.views import View
from django.http import HttpResponse
from django.conf import settings

from . import models

def decapsulate_body(request):
    """Returns the body of a Request object with MIME encapulation
    removed if any

    Leading and trailling whitespace is also removed fromthe output
    """
    lineboundary= b'\r\n' # From HTTP Spec
    if request.headers.get('Content-Type',None):
        bodylines = request.body.split(lineboundary)
        #Find the last non-blankline, and stop if we get tothe top
        lastline = len(bodylines) -1
        while lastline > 0  and bodylines[lastline] == b'':
            lastline -= 1
        # Compare the two boudnary lines match but onlyif they
        # are not the same line
        if lastline == 0 or bodylines[0] != bodylines[lastline]:
            return request.body.strip()
        return lineboundary.join(bodylines[1:lastline]).strip()
    else:
        return request.body.strip()


class ConsentView(View):
    status_flag = None
    def post(self, request, token):
        models.ConsentRecord.objects.create(
            token = token,
            referrer = request.META['HTTP_REFERRER'],
            user_agent = request.headers['User-Agent'],
            status = decapsulate_body(request),
            status_flag = self.status_flag,
        )
        if settings.CONSENT_LOG_AUTO_EXPIRE:
            models.expire_consent_log(reason = "Auto Expiry")
        return HttpResponse('')


class ConfirmView(ConsentView):
    status_flag = True
class RejectView(ConsentView):
    status_flag = False
