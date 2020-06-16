from django.core.management.base import BaseCommand, CommandError
from ... import models


class Command(BaseCommand):
    help = '''Does a expiry run on the consent log if the current
    expiry run policy is met
    '''
    def add_arguments(self, parser):
        parser.add_argument('--force', action='store_true',
                            help = "Run and expiry pass of the consent log if if one has been run recently"
                            )

        parser.add_argument('--reason', type=str, nargs='?', default='Command line launch',
                            help="Reason for the consent log expiry run. Used for logging only")

    def handle(self, *args, **kwargs):
        models.expire_consent_log(**kwargs)
