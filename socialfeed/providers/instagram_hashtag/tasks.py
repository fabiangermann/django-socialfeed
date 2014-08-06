import pytz

from celery import shared_task
from instagram import InstagramAPI

from socialfeed.models import Subscription, Post


@shared_task
def process_instagram_update(update):
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
            created_at=image.created_time.replace(tzinfo=pytz.utc)
        )

        if not created:
            continue

        post.data = {
            'filter': image.filter,
            'link': image.link,
            'type': image.type,
            'tags': [t.name for t in image.tags],
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
