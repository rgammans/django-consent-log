""" Consent Log is a simple model to store record of consent actions.

Specifcally the following information is stored

    The first three octets  of a user's IP addresss.
    The date and time of the consent.
    User agent string sent with the notification request.
    The Referrer header sent with the noticication request.
    An unique id generated on the frontend. This serves to identify the consenting individial.
    The user's consent state, serving as proof of consent.

"""

from django.test import TestCase

class ConsentLog(TestCase):

    def test_request_confirm_stores_a_the_above_in_the_model_and_consent_is_true(self,):
        pass
    def test_request_revoke_stores_a_the_above_in_the_model_and_consent_is_true(self,):
        pass
