class BaseProvider(object):
    @classmethod
    def label(cls):
        raise NotImplementedError

    @property
    def config_fields(self):
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
