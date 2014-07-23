from django.core.management.base import BaseCommand

from instagram.client import InstagramAPI

from socialfeed.models import Subscription

class Command(BaseCommand):
    def handle(self, app_id=None, app_secret=None, subscription_id=None, *args, **kwargs):
        if app_id and app_secret and subscription_id:

            api = InstagramAPI(
                client_id=app_id,
                client_secret=app_secret)
            print '\nDeleting subscription {}'.format(subscription_id)
            api.delete_subscriptions(id=subscription_id)
