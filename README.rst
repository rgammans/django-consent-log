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
value `CONSENT_LOG_DAYS_EXPIRY` to settings.py to configure
the length of time to to records for

If you user the expire_consent_log() model function , or expireconset
management command you can set a maximum frequency at which the 
the expire run will happen.  
CONSENT_LOG_EXPIRY_MIN_PERIOD = 7 # Only run expiry once a week maxmum.

you must set ths variable if you use these entrypoints

CONSENT_LOG_AUTO_EXPIRE, attempts a 

