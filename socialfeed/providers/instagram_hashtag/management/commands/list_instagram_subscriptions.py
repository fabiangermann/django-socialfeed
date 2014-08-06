from django.core.management.base import BaseCommand

from instagram.client import InstagramAPI

from socialfeed.models import Subscription


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        subscriptions = Subscription.objects.filter(provider__in=[
            'socialfeed.providers.instagram_hashtag'
        ])

        processed_apps = []
        for subscription in subscriptions:
            app_id = subscription.config.get('app_id')
            app_secret = subscription.config.get('app_secret')

            if app_id and app_secret and app_id not in processed_apps:
                api = InstagramAPI(
                    client_id=app_id,
                    client_secret=app_secret)
                print '\nSubscriptions for app {}'.format(app_id)
                print api.list_subscriptions()

                processed_apps.append(app_id)
