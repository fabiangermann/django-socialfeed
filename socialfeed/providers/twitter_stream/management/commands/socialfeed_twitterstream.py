from django.core.management.base import BaseCommand, CommandError

from socialfeed.providers.twitter_stream.streamer import Streamer

from socialfeed.models import Subscription

class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        try:
            subscription_id = args[0]
        except IndexError:
            raise CommandError('Please provider subscription id as first '
                               'argument')

        try:
            subscription = Subscription.objects.get(
                pk=subscription_id,
                provider='socialfeed.providers.twitter_stream',
                is_active=True)
        except Subscription.DoesNotExist:
            valid_subscriptions = Subscription.objects.filter(
                provider='socialfeed.providers.twitter_stream',
                is_active=True)

            valid_subscriptions = '\n'.join(
                ['ID: {0}, Title: {1}'.format(s.id, s.title)
                    for s in valid_subscriptions])

            raise CommandError('No matching subscription found. Please make '
                               'sure the provided id does exist, the '
                               'subscription is active and has the correct '
                               'provider is assigned.\n\nValid subscriptions '
                               'are:\n{}'.format(valid_subscriptions))

        streamer = Streamer(
            subscription.config['api_key'],
            subscription.config['api_secret'],
            subscription.config['access_token'],
            subscription.config['access_token_secret'],
            subscription=subscription)

        streamer.statuses.filter(track=subscription.config['filter'])
