from django.core.management.base import BaseCommand

from socialfeed.providers.twitter_stream.streamer import Streamer

from socialfeed.models import Subscription

class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        subscription = Subscription.objects.filter(
            provider='socialfeed.providers.twitter_stream',
            is_active=True).first()

        streamer = Streamer(
            subscription.config['api_key'],
            subscription.config['api_secret'],
            subscription.config['access_token'],
            subscription.config['access_token_secret'],
            subscription=subscription)

        streamer.statuses.filter(track=subscription.config['filter'])
