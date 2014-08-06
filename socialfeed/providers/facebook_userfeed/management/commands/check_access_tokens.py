from datetime import datetime
from django.core.management.base import BaseCommand

from facepy import GraphAPI

from socialfeed.models import Subscription


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        subscriptions = Subscription.objects.filter(
            provider__in=['socialfeed.providers.facebook_userfeed'])

        for subscription in subscriptions:
            if not all(key in subscription.config for key in ['app_id',
                                                              'app_secret',
                                                              'access_token']):
                continue

            access_token = '|'.join([subscription.config['app_id'],
                                     subscription.config['app_secret']])
            input_token = subscription.config['access_token']

            api = GraphAPI(access_token)
            result = api.get('/debug_token?input_token={}'.format(input_token))

            self.stdout.write('''
            Subscription: {subscription}
            Facebook App: {app} ({app_id})
            Token expires: {expires}
            Token valid: {valid}
            Error: {error}\n
            '''.format(**{
                'subscription': subscription,
                'app': result['data']['application'],
                'app_id': result['data']['app_id'],
                'valid': result['data']['is_valid'],
                'expires': datetime.fromtimestamp(
                    result['data']['expires_at']),
                'error': result['data'].get('error', {}).get('message')
            }))
