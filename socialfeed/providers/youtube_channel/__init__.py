import json

from django.utils.translation import ugettext_lazy as _

from socialfeed.providers import BaseProvider

from apiclient.discovery import build


class Provider(BaseProvider):
    @classmethod
    def get_label(cls):
        return _('Youtube (channel)')

    @classmethod
    def get_config_fields(self):
        return ['api_key', 'channel_id']

    def subscribe(self):
        return None

    def unsubscribe(self):
        return None

    def pull_posts(self):

        self.service = build(
            'youtube', 'v3', developerKey=self.subscription.config['api_key'])

        channels = self.service.channels().list(
            part='contentDetails',
            id=self.subscription.config['channel_id']).execute()
        channel = channels['items'][0]

        playlist_id = channel['contentDetails']['relatedPlaylists']['uploads']

        self.fetch_uploads(playlist_id)

    def fetch_uploads(self, playlist_id, page_token=None):
        from socialfeed.models import Post

        if page_token:
            uploads = self.service.playlistItems().list(
                part='snippet',
                playlistId=playlist_id,
                pageToken=page_token).execute()
        else:
            uploads = self.service.playlistItems().list(
                part='snippet',
                playlistId=playlist_id).execute()

        for upload in uploads['items']:
            post, created = Post.objects.get_or_create(
                subscription=self.subscription,
                source_id=upload['snippet']['resourceId']['videoId'])
            if not created:
                continue

            post.data = upload['snippet']
            post.save()

        if 'nextPageToken' in uploads:
            self.fetch_uploads(playlist_id, uploads['nextPageToken'])

    def get_post_thumbnail(self, post):
        return post.data.get('thumbnails', {}).get('default', {}).get('url')

    def get_post_title(self, post):
        return post.data.get('title')
