from twython import TwythonStreamer

from socialfeed.models import Post
from socialfeed.providers import BaseProvider


class Streamer(TwythonStreamer):
    def __init__(self, *args, **kwargs):

        self.subscription = kwargs.pop('subscription')

        return super(Streamer, self).__init__(*args, **kwargs)

    def on_success(self, data):
        post, created = Post.objects.get_or_create(
            subscription=self.subscription,
            source_id=data['id']
        )

        # Skip tweets already fetched
        if not created:
            return

        post.data = data
        post.save()

    def on_error(self, status_code, data):
        #print 'ERROR', status_code, data
        pass

