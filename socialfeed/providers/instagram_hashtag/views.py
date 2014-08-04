import json
import sys
import logging

from django.http import HttpResponse
from django.views.generic import View

from instagram import InstagramAPI, subscriptions

from socialfeed.models import Subscription, Post

reactor = subscriptions.SubscriptionsReactor()

logger = logging.getLogger(__name__)

class InstagramPush(View):
    def get(self, request, **kwargs):
        return HttpResponse(request.GET.get('hub.challenge', 'error'))

    def post(self, request, subscription_pk, **kwargs):
        x_hub_signature = request.META.get('HTTP_X_HUB_SIGNATURE')
        raw_response = request.body
        try:
            subscription = Subscription.objects.get(pk=subscription_pk)
            reactor.process(
                subscription.config['app_secret'], raw_response, x_hub_signature)
        except Exception:
            print 'Got error in reactor processing: %s' % raw_response
            exc_type, exc_value, exc_traceback = sys.exc_info()
            print exc_type, exc_value
        return HttpResponse('ok')


def processInstagramUpdate(update):
    subscription_id = update.get('subscription_id')
    subscription = Subscription.objects.filter(
        subscription_id=subscription_id).first()

    if not subscription:
        return

    api = InstagramAPI(
        client_id=subscription.config.get('app_id'),
        client_secret=subscription.config.get('app_secret'))

    tag = update['object_id']
    media, next = api.tag_recent_media(30, 0, tag)

    for image in media:
        post, created = Post.objects.get_or_create(
            subscription=subscription,
            source_id=image.id,
            created_at=image.created_time
        )

        if not created:
            continue

        post.data = {
            'created_time': str(image.created_time),
            'filter': image.filter,
            'link': image.link,
            'type': image.type,
            'tags': [tag.name for tag in image.tags],
            'user': {
                'id': image.user.id,
                'username': image.user.username,
                'full_name': image.user.full_name,
                'profile_picture': image.user.profile_picture,
                'website': image.user.website,
                'bio': image.user.bio,
            },
            'images': {
                'thumbnail': image.get_thumbnail_url(),
                'small': image.get_low_resolution_url(),
                'default': image.get_standard_resolution_url(),
            }
        }
        if getattr(image, 'caption', None):
            post.data['caption'] = image.caption.text

        if getattr(image, 'location', None) \
            and getattr(image.location, 'point', None):
                post.data['location'] = {
                    'latitude': image.location.point.latitude,
                    'longitude': image.location.point.longitude,
                }

        post.save()


reactor.register_callback(subscriptions.SubscriptionType.USER,
                          processInstagramUpdate)
reactor.register_callback(subscriptions.SubscriptionType.TAG,
                          processInstagramUpdate)
