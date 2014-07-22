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

    def __init__(self, subscription, *args, **kwargs):
        self.subscription = subscription
        super(BaseProvider, self).__init__(*args, **kwargs)

    def subscribe(self):
        app_id = self.subscription.config['app_id']
        app_secret = self.subscription.config['app_secret']

        access_token = '{app_id}|{app_secret}'.format(**{
            'app_id': app_id,
            'app_secret': app_secret
        })
        api = GraphAPI(access_token)

        callback_url = 'http://{}{}'.format(
            Site.objects.get_current().domain,
            reverse('socialfeed_facebook_push'))
        response = api.post(
            '{0}/subscriptions'.format(app_id,),
            object='user',
            callback_url=callback_url,
            fields='feed',
            verify_token=self.subscription.id
        )

    def unsubscribe(self):
        raise NotImplementedError

    def pull_posts(self):
        from socialfeed.models import Post
        api = GraphAPI(self.subscription.config['access_token'])

        feed = api.get('me/posts')
        for feed_item in feed['data']:
            if feed_item.get('status_type') not in ['mobile_status_update',
                                                    'added_photos']:
                continue

            post, created = Post.objects.get_or_create(
                subscription=self.subscription,
                source_id=feed_item.get('id'))

            if not created:
                continue

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
