Django Consent Log
------------------

.. image:: https://github.com/rgammans/django-consent-log/workflows/Project%20tests/badge.svg


Some django views which log actions taken on the frontend, these return an emtpy HTML page and are intended
to be called from an ajax function on the frontend. No frontent functions are provided but there are many cookie
and other consent banner action projects on npmjs.com which can be use the build the frontend component.

The  timestamp, user agent string, referrer are stored along with a boolean flag for consent /reject
status. Additionally the request body is also stored so the frontend can send supplemental data to store.

An expiry framework is included which provides a mechanism for deletion of records older than 
a certain, the rentenion period can be set in the settings.py file. The expiry framework 
also has a mechanism to limit it runs to a maximum frequency.

Anonymized IP address storage is planned but not yet implemented. 

This provides the views and the management logs for
the purpose

Setup
-----

Add::

    'consent_log'


to ``INSTALLED_APPS`` in settings.py and also a set an integer
value ``CONSENT_LOG_DAYS_EXPIRY`` to settings.py to configure
the length of time that consent record live for.

You must also set the boolean value ``CONSENT_LOG_AUTO_EXPIRE``, this
setting is treated as a booleand and if true expire_consent_log() is call
on every request to the confirm or reject views. 

If you use the ``expire_consent_log()`` model function (such as via the auto
expire setting above), or expireconset management command you can set a
maximum frequency at which the the expire run will happen.  

::

    CONSENT_LOG_EXPIRY_MIN_PERIOD = 7 # Only run expiry once a week maxmum.

you must set ths variable if you use these entrypoints.

To Use
------

Add something like the following to your projects urls.py..

::

    path("consent_log/", include("consent_log.urls"))

This add the modules endpoints to your defined urls, our urls are
reversable and named ``consent-log:confirm`` and 'consent-log:reject`` within
django url namespace so can be reference as those insire your django templates.

You will need to write or import your own frontend integration 
to send the actions to record to this module.


