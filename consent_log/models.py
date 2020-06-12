from django.db import models
from .apps import app_name

class ConsentRecord(models.Model):
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

