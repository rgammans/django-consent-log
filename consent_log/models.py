from django.db import models
from django.conf import settings
from .apps import app_name
import datetime


def expire_consent_log(**kwargs ):
    """Delete on and expired reords in the ConsentLog. If time for a expiry run.

    This is an entry point for checking any configured expiry policy
    before running the consetn expiry functions.

    """
    reason = kwargs.get('reason','unspecified')
    force = kwargs.get('force',False)
    run_threshold = datetime.datetime.now() - datetime.timedelta(days = settings.CONSENT_LOG_EXPIRY_MIN_PERIOD)
    if force or not ExpiryLog.objects.filter(date_run__gt = run_threshold).exists():
        ExpiryLog.objects.create(run_reason=reason)
        ConsentRecord.objects.delete_expired()

class ExpiryLog(models.Model):
    date_run = models.DateTimeField(auto_now_add = True)
    run_reason = models.CharField(max_length =200)


class ConsentQuerySet(models.QuerySet):
    def delete_expired(self,):
        expires = datetime.datetime.now() - datetime.timedelta(days = settings.CONSENT_LOG_DAYS_EXPIRY)
        return self.filter(confirmed_on__lt = expires).delete()

class ConsentRecord(models.Model):

    objects = ConsentQuerySet.as_manager()

    token = models.CharField(max_length =512)
    confirmed_on = models.DateTimeField(auto_now_add = True)
    ip_address= models.BinaryField( max_length = 16 )
    # These values come from HTTP Headers.abs
    # The Http spec itself has no max header
    # size, bu the largest header size is in
    # tomcat at 48K. But that a)) excessive
    # and B) django app are rarely served by
    # tomact so we will use the next highest 
    # which is IIS at 16K.
    referrer = models.CharField(max_length = 16384) 
    user_agent= models.CharField(max_length = 16384)
    status_flag = models.BooleanField()
    status = models.BinaryField()

