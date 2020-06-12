Django Consent Log
------------------

Some views which log actions taken on the frontend.

A timestamp, ip subnet (/24 prefix only) user agent string
and status are stored.


IP address storage is note yet implemented

This provides the views and the management logs for
the purpose

Setup
-----

Add 

```
    'Consent_log'
```

to INSTALLED_APPS in settinfs.py and also a da integet
value `CONSENT_DAYS_EXPIRY` to settings.py to configure
the length of time to to records for
