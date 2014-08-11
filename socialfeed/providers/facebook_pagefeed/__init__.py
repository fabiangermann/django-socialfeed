import calendar
from datetime import datetime, timedelta

from django import forms
from django.utils.translation import ugettext_lazy as _

from facepy import GraphAPI

from socialfeed.providers import BaseProvider


TYPE_CHOICES = (
    ('all', _('All posts')),
    ('posts', _('Only posts published by this page.')),
    ('tagged', _('Only posts this page was tagged in.')),
)


class Provider(BaseProvider):
    @classmethod
    def get_label(cls):
        return 'facebook (page feed)'

    @classmethod
    def get_config_fields(self):
        return (
            ['app_id', forms.CharField],
            ['app_secret', forms.CharField],
            ['page_id', forms.CharField],
            # TODO: Implement filtering for "/{page_id}/posts",
            # "/{page_id}/tagged" and maybe "/{page_id}/promotable_posts".
            # API reference: https://developers.facebook.com/docs/graph-api/
            # reference/v2.0/page/feed/
            # ['filter', forms.ChoiceField, {'choices': TYPE_CHOICES}],
        )

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

    # TODO: Implement paging
    def pull_posts(self):
        '''
        Pull posts from the page's feed. At the moment the following post
        types are supportd:
            - normal status updates (type: status, status_type:
                mobile_status_update)
            - posting of single images (type: photo, status_type:
                added_photos)
            - posting of multiple images. But only the first image will be
                available (type: photo, status_type: added_photos).
        '''
        from socialfeed.models import Post
        access_token = '|'.join([self.subscription.config['app_id'],
                                 self.subscription.config['app_secret']])
        api = GraphAPI(access_token)

        now = calendar.timegm(datetime.utcnow().timetuple())
        try:
            since = self.subscription.config['last_pull']
            since = datetime.utcnow() - timedelta(days=30)
            since = calendar.timegm(since.timetuple())
        except KeyError:
            since = datetime.utcnow() - timedelta(days=30)
            since = calendar.timegm(since.timetuple())

        feed = api.get('{}/feed'.format(self.subscription.config['page_id']))

        for feed_item in feed['data']:
            # Skip unsupported types
            if feed_item.get('status_type') not in ['mobile_status_update',
                                                    'added_photos']:
                continue

            # Skip if post already exists
            post, created = Post.objects.get_or_create(
                subscription=self.subscription,
                source_id=feed_item.get('id'),
                created_at=feed_item.get('created_time'))
            if not created:
                continue

            # Get post data
            post.data = {
                'created_time': str(feed_item.get('created_time')),
                'type': feed_item.get('type'),
                'status_type': feed_item.get('status_type'),
                'story': feed_item.get('story'),
                'link': feed_item.get('link'),
                'message': feed_item.get('message'),
            }

            if feed_item['type'] == 'status':
                # nothing special here
                pass

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

        self.subscription.config['last_pull'] = now
        self.subscription.save()

    def get_post_thumbnail(self, post):
        return post.data.get('images', {}).get('thumbnail')

    def get_post_title(self, post):
        return '{0} ({1})'.format(post.data.get('status_type'), post.source_id)
