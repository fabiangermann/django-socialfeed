from socialfeed.providers import BaseProvider

from django.utils.translation import ugettext_lazy as _


class Provider(BaseProvider):
    @classmethod
    def get_label(cls):
        return _('Twitter (stream)')

    @classmethod
    def get_config_fields(self):
        return ['api_key', 'api_secret', 'access_token', 'access_token_secret',
                'filter']

    def subscribe(self):
        return

    def unsubscribe(self):
        return

    def pull_posts(self):
        return

    def get_post_thumbnail(self, post):
        for media in post.data['entities'].get('media', []):
            if not media['type'] == 'photo':
                continue

            return media['media_url_https']
            break
        else:
            return None

    def get_post_title(self, post):
        return post.data.get('text')
