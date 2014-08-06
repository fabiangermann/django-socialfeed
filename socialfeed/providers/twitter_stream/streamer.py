import json
import pytz

from time import strptime
from datetime import datetime

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

        # Assign data returned from twitter
        post.data = data

        # Dont bother with conversion of the creation date form data as its a
        # livestream anyway.
        ch = pytz.timezone('Europe/Zurich')
        post.created_at = datetime.now(tz=ch)

        post.save()

    def on_error(self, status_code, data):
        #print 'ERROR', status_code, data
        pass
