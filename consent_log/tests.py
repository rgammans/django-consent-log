""" Consent Log is a simple model to store record of consent actions.

Specifcally the following information is stored

    The first three octets  of a user's IP addresss.
    The date and time of the consent.
    User agent string sent with the notification request.
    The Referrer header sent with the noticication request.
    An unique id generated on the frontend. This serves to identify the consenting individial.
    The user's consent state, serving as proof of consent.

"""
import unittest
import unittest.mock
import datetime
from django.test import TestCase, RequestFactory, Client
from django import urls
from django.conf import settings

from django.conf import settings
from consent_log import models
from consent_log import views

class ConsentLogRequestTests(TestCase):
    user_agent_string = "A Dummy Mozilla/5.0 (like user agent string Win/Foo Bar/baz)"
    referrer = 'http://some.site/index.html'
    body = b'xxx'

    def make_request(self, endpoint, testname, content_type = "application/foo"):
        token = f"{testname}_1234567890-asdfghj"
        c = Client(
            HTTP_USER_AGENT =  self.user_agent_string,
            HTTP_REFERRER = self.referrer
        )
        response = c.post(
            urls.reverse( f'consent_log:{endpoint}', kwargs={'token': token}),
            content_type = content_type,
            data = self.body
        )
        return token, response

    def test_confirm_request_can_be_made(self,):
        token, response = self.make_request("confirm","confirm_request_can_be_made")
        self.assertEqual(response.status_code, 200)

    def test_confirm_request_stores_the_data_in_the_model_and_consent_is_corect_value(self,):
        self.dotest_request_stores_the_data_in_the_model_and_consent_is_corect_value("confirm","confirm_request_can_be_made", True)

    def test_reject_request_stores_the_data_in_the_model_and_consent_is_corect_value(self,):
        self.dotest_request_stores_the_data_in_the_model_and_consent_is_corect_value("reject","reject_request_can_be_made", False)

    def test_reject_request_calls_expire_consent_log_if_auto_expire_set(self,):
        settings.CONSENT_LOG_AUTO_EXPIRE= True
        with  unittest.mock.patch.object(models,'expire_consent_log') as ecl:
            self.dotest_request_stores_the_data_in_the_model_and_consent_is_corect_value("reject","reject_request_can_be_made", False)
        ecl.assert_called_with(reason = "Auto Expiry")


    def test_confirm_request_calls_expire_consent_log_if_auto_expire_set(self,):
        settings.CONSENT_LOG_AUTO_EXPIRE= True
        with  unittest.mock.patch.object(models,'expire_consent_log') as ecl:
            self.dotest_request_stores_the_data_in_the_model_and_consent_is_corect_value("confirm","confirm_auto-expires", True)
        ecl.assert_called_with(reason = "Auto Expiry")

    def test_reject_request_deosnt_calls_expire_consent_log_if_auto_expire_unset(self,):
        settings.CONSENT_LOG_AUTO_EXPIRE= False
        with  unittest.mock.patch.object(models,'expire_consent_log') as ecl:
            self.dotest_request_stores_the_data_in_the_model_and_consent_is_corect_value("reject","reject_request_can_be_made", False)
        ecl.assert_not_called()


    def test_confirm_request_doesntcalls_expire_consent_log_if_auto_expire_unset(self,):
        settings.CONSENT_LOG_AUTO_EXPIRE= False
        with  unittest.mock.patch.object(models,'expire_consent_log') as ecl:
            self.dotest_request_stores_the_data_in_the_model_and_consent_is_corect_value("confirm","conrirm_auto-expires", True)
        ecl.assert_not_called()



    def dotest_request_stores_the_data_in_the_model_and_consent_is_corect_value(self,url,testname ,consentValue):
        log_entries_known = set(models.ConsentRecord.objects.all().values_list('pk'))
        token, response = self.make_request(url,testname)
        new_log_entries = set(models.ConsentRecord.objects.all().values_list('pk'))
        new_entry = new_log_entries - log_entries_known
        self.assertEqual(len(new_entry),1)
        new_entry = next(iter(new_entry))
        new_record = models.ConsentRecord.objects.get(pk=new_entry[0])
        self.assertEqual(new_record.token,token)
        self.assertEqual(new_record.referrer, self.referrer)
        self.assertEqual(new_record.user_agent, self.user_agent_string)
        self.assertEqual(new_record.status, self.body)
        self.assertEqual(new_record.status_flag,consentValue)
        delay = datetime.datetime.now() - new_record.confirmed_on
        # Check within last second
        self.assertLessEqual(delay, datetime.timedelta(seconds=1))

    def test_request_doesnt_crash_with_oversized_header(self,):  ## This need to check for eahc hader
        oversized_len =  65536
        self.user_agent_string = ''.join( [ 'x'] * oversized_len)
        self.dotest_request_stores_the_data_in_the_model_and_consent_is_corect_value("reject","reject_request_can_be_made", False)

    @unittest.skip('''
            Before this is usefule we should decide what counts as an oversized body,
            and of a size need to be able to handle

            Most frontend webservers set a content input limit anyway.
    ''')
    def test_request_doesnt_crash_with_oversized_bodies(self,):
        oversized_len =  65
        self.body = b''.join( [ b'x'] * oversized_len)
        self.dotest_request_stores_the_data_in_the_model_and_consent_is_corect_value("reject","reject_request_can_be_made", False)


class ConsentLogQuerySetTests(TestCase):
   
    def setUp(self,):
        #TODO read from settings
        self.expiry_days = settings.CONSENT_LOG_DAYS_EXPIRY
        blocksz = 10
        self.length = self.expiry_days // (blocksz // 2)
#        expiry = datetime.timedelta(days=expiry_days)
        nxtdelay =datetime.timedelta(days = blocksz)
        ts = datetime.datetime.now()
        for i in range(self.length):
            r = models.ConsentRecord.objects.create(
                confirmed_on = ts,
                token = f"tst{i}",
                user_agent = "use user_agent",
                status=b"Yes",
                status_flag =  True,
                referrer = ""
            )
            # Force tsimestamp
            r.confirmed_on = ts
            r.save()
            ts = ts - nxtdelay

 
    def test_delete_expired_deletes_expired_records_and_keeps_unexpired(self,):
        models.ConsentRecord.objects.delete_expired()
        self.assertGreater( min(r.confirmed_on 
            for r in models.ConsentRecord.objects.all()
        ), datetime.datetime.now() - datetime.timedelta(days= self.expiry_days))
        ## It should be exactly half but we need to cope with length being odd
        #  so we compare > 40% and < 60%. When dhoe be find as long a length> 10
        self.assertLess(models.ConsentRecord.objects.all().count(),self.length*.6)
        self.assertGreater(models.ConsentRecord.objects.all().count(),self.length*.4)


class MockRequest:
    def __init__(self,body, use_mime = False):
        self.headers = {}
        self.boundary=b"--This is a Boundary--\r\n"
        if use_mime:
            self.headers['Content-Type'] = "application/foo"
        else:
            self.boundary=b""
        self.body = self.boundary+body+b'\r\n'+self.boundary

class UtilFunctionsTests(TestCase):
    def setUp(self,):
        self.body = b'Testmessage'

    def test_decapsulate_body_without_mime(self,):
        req = MockRequest(self.body)
        self.assertEqual(views.decapsulate_body(req),self.body)

    def test_decapsulate_body_with_mime(self,):
        req = MockRequest(self.body, use_mime = True)
        self.assertEqual(views.decapsulate_body(req),self.body)

    def test_decapsulate_body__with_invalid_mime_returns_whole_body(self,):
        req = MockRequest(self.body, use_mime = True)
        req.body=req.body[:-6]+b'\r\n'
        self.assertEqual(views.decapsulate_body(req),req.body.strip())

    def test_decapsulate_body_returns_boundaries_without_content_type(self,):
        req = MockRequest(self.body, use_mime = True)
        body = req.body
        del req.headers['Content-Type']
        self.assertEqual(views.decapsulate_body(req),body.strip())


class ExpireConsetLogTests(TestCase):

    def test_expire_consent_log_calls_qs_delete_expired(self,):
        with unittest.mock.patch.object(models.ConsentRecord.objects,'delete_expired') as de:
            models.expire_consent_log()

        de.assert_called_once()

    def test_expire_consent_log_inserts_into_the_expiry_log(self,):
        records = models.ExpiryLog.objects.all().count()
        models.expire_consent_log()
        self.assertEqual(models.ExpiryLog.objects.all().count(),records + 1)

    def test_expire_conset_log_inserts_into_the_expiry_log_with_passed_reason_value(self,):
        reason = "Test reason for expiry"
        log_entries_known = set(models.ExpiryLog.objects.all().values_list('pk'))
        models.expire_consent_log(reason = reason)
        new_logs = set(models.ExpiryLog.objects.all().values_list('pk'))
        new_entry = new_logs -  log_entries_known
        self.assertEqual(len(new_entry),1)
        new_entry = next(iter(new_entry))
        new_record = models.ExpiryLog.objects.get(pk=new_entry[0])
        self.assertEqual(new_record.run_reason,reason)

    def test_expire_cosent_log_deosnt_run_if_there_is_reecent_expiry(self,):
        ##Nb test app sett max Period to 7 days.abs
        models.ExpiryLog.objects.create(run_reason="dummy run for test")
        with unittest.mock.patch.object(models.ConsentRecord.objects,'delete_expired') as de:
            models.expire_consent_log()

        de.assert_not_called()

    def test_expire_cosent_log_deos_run_if_there_is_reecent_expiry_but_force_is_specified(self,):
        ##Nb test app sett max Period to 7 days.abs
        models.ExpiryLog.objects.create(run_reason="dummy run for test")
        with unittest.mock.patch.object(models.ConsentRecord.objects,'delete_expired') as de:
            models.expire_consent_log(force= True)

        de.assert_called_once()
