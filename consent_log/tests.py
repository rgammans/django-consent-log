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
from django.test import TestCase, RequestFactory, Client
from django import urls

class ConsentLog(TestCase):

    def test_confirm_request_can_be_made(self,):
        user_agent_string = "A Dummy Mozilla/5.0 (like user agent string Win/Foo Bar/baz)"
        referrer = 'http://some.site/index.html'
        token = "test_confirm_request_can_be_made_1234567890-asdfghj"
        c = Client(
            HTTP_USER_AGENT =  user_agent_string,
            HTTP_REFERRER = referrer
        )
        response = c.post(urls.reverse('consent_log:confirm', kwargs={'token': token}))
        self.assertEqual(response.status_code, 200)

    @unittest.skip('nyi')
    def test_request_confirm_stores_a_the_above_in_the_model_and_consent_is_true(self,):
        self.fail()

    @unittest.skip('nyi')
    def test_request_revoke_stores_a_the_above_in_the_model_and_consent_is_true(self,):
        self.fail()
