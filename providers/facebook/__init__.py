from socialfeed.providers import BaseProvider


class Provider(BaseProvider):
    @classmethod
    def get_label(cls):
        return 'facebook (user feed)'

    @classmethod
    def get_config_fields(self):
        return ['app_id', 'app_secret', 'redirect_uri']

    def __init__(self, subscription, *args, **kwargs):
        self.subscription = subscription
        super(BaseProvider, self).__init__(*args, **kwargs)

    def subscribe(self):
        raise NotImplementedError

    def unsubscribe(self):
        raise NotImplementedError

    def pull_posts(self):
        raise NotImplementedError

    def get_post_thumbnail(self, post):
        raise NotImplementedError

    def get_post_title(self, post):
        raise NotImplementedError

