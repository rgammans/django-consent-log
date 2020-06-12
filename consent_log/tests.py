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
import datetime
from django.test import TestCase, RequestFactory, Client
from django import urls

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

    @unittest.skip('need to decide what counts as an oversized body. The Web frontedn normallr rekects those')
    def test_request_doesnt_crash_with_oversized_bodies(self,):
        oversized_len =  65
        self.body = b''.join( [ b'x'] * oversized_len)
        self.dotest_request_stores_the_data_in_the_model_and_consent_is_corect_value("reject","reject_request_can_be_made", False)




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
