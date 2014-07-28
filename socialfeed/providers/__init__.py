class BaseProvider(object):
    @classmethod
    def get_label(cls):
        raise NotImplementedError

    @classmethod
    def get_config_fields(self):
        raise NotImplementedError

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
