from django import forms
from django.utils.translation import ugettext_lazy as _

from socialfeed.providers import BaseProvider


class Provider(BaseProvider):
    @classmethod
    def get_label(cls):
        return _('Twitter (stream)')

    @classmethod
    def get_config_fields(self):
        return (
            ['api_key', forms.CharField],
            ['api_secret', forms.CharField],
            ['access_token', forms.CharField],
            ['access_token_secret', forms.CharField],
            ['filter', forms.CharField]
        )

    def subscribe(self):
        return

    def unsubscribe(self):
        return

    def pull_posts(self):
        return

    def get_post_thumbnail(self, post):
        for media in post.data.get('entities', {}).get('media', []):
            if not media['type'] == 'photo':
                continue

            return media['media_url_https']
            break
        else:
            return None

    def get_post_title(self, post):
        return post.data.get('text')
