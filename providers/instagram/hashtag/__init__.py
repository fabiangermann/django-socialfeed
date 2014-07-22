from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _

from instagram.client import InstagramAPI

from socialfeed.providers import BaseProvider


class Provider(BaseProvider):
    @classmethod
    def get_label(cls):
        return _('instagram (hashtag)')

    @classmethod
    def get_config_fields(cls):
        return ['hashtag', 'app_id', 'app_secret',
                'app_callback_url']

    def subscribe(self):
        api = InstagramAPI(
            client_id=self.subscription.config['app_id'],
            client_secret=self.subscription.config['app_secret'])

        result = api.create_subscription(
            object='tag',
            object_id=self.subscription.config['hashtag'],
            aspect='media',
            callback_url='{callback_url}{verify_url}'.format(**{
                'callback_url': self.subscription.config['app_callback_url'],
                'verify_url': reverse(
                    'instagram_verify_subscription',
                    kwargs={'subscription_pk': self.subscription.pk}
                )
            }))
        self.subscription.subscription_id = result['data']['id']
        self.subscription.save()

        print result

    def unsubscribe(self):
        api = InstagramAPI(
            client_id=self.subscription.config['app_id'],
            client_secret=self.subscription.config['app_secret'])

        result = api.delete_subscriptions(
            id=self.subscription.subscription_id)

        print result

    def get_post_thumbnail(self, post):
        return post.data.get('images', {}).get('thumbnail')

    def get_post_title(self, post):
        return post.data.get('caption', '')
