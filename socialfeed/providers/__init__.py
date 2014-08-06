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
        '''
        Called when the is_active flag is set from false to true (on save).

        DO NOT save the subscription in this method!
        '''
        raise NotImplementedError

    def unsubscribe(self):
        '''
        Called when the is_active flag is set from true to false (on save)
        and when subscription is delted.

        DO NOT save the subscription in this method!
        '''
        raise NotImplementedError

    def pull_posts(self):
        raise NotImplementedError

    def get_post_thumbnail(self, post):
        raise NotImplementedError

    def get_post_title(self, post):
        raise NotImplementedError
