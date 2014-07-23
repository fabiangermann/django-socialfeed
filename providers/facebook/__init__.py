import json

from django.contrib.sites.models import Site
from django.core.urlresolvers import reverse

from facepy import GraphAPI

from socialfeed.providers import BaseProvider


class Provider(BaseProvider):
    @classmethod
    def get_label(cls):
        return 'facebook (user feed)'

    @classmethod
    def get_config_fields(self):
        return ['app_id', 'app_secret']

    def subscribe(self):
        '''
        Real time updates (https://developers.facebook.com/docs/
        graph-api/real-time-updates/v2.0) not implemented.
        '''
        return None

    def unsubscribe(self):
        '''
        Real time updates (https://developers.facebook.com/docs/
        graph-api/real-time-updates/v2.0) not implemented.
        '''
        return None

    def pull_posts(self):
        '''
        Pull posts from the users feed. At the moment only posts with
        status_type 'mobile_status_update' or 'added_photos' are
        supported
        '''
        from socialfeed.models import Post
        api = GraphAPI(self.subscription.config['access_token'])

        feed = api.get('me/posts')
        for feed_item in feed['data']:
            # Skip unsupported types
            if feed_item.get('status_type') not in ['mobile_status_update',
                                                    'added_photos']:
                continue

            # Skip if post already exists
            post, created = Post.objects.get_or_create(
                subscription=self.subscription,
                source_id=feed_item.get('id'))
            if not created:
                continue

            # Get post data
            post.data = {
                'created_time': str(feed_item.get('created_time')),
                'type': feed_item.get('type'),
                'status_type': feed_item.get('status_type'),
                'story': feed_item.get('story'),
                'link': feed_item.get('link'),
            }

            if feed_item['type'] == 'status':
                post.data.update({
                    'message': feed_item.get('message'),
                    'status_type': feed_item.get('status_type')
                })

            if feed_item['type'] == 'photo':
                try:
                    photo = api.get(feed_item['object_id'])
                    post.data.update({
                        'name': photo.get('name'),
                        'images': {
                            'thumbnail': photo['picture'],
                            'default': photo['source']
                        }
                    })
                except:
                    pass
            post.save()

    def get_post_thumbnail(self, post):
        return post.data.get('images', {}).get('thumbnail')

    def get_post_title(self, post):
        return '{0} ({1})'.format(post.data.get('status_type'), post.source_id)
