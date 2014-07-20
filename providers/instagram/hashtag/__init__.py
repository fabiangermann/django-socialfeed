from django.utils.translation import ugettext_lazy as _

from socialfeed.providers import BaseProvider


class Provider(BaseProvider):
    @classmethod
    def label(cls):
        return _('instagram (hashtag)')

    @property
    def config_fields(self):
        return ['hashtag']

    def subscribe(self):
        print self.subscription
