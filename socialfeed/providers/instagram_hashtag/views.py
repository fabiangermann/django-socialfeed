import sys
import logging

from django.http import HttpResponse
from django.views.generic import View

from instagram import subscriptions

from socialfeed.models import Subscription

from .tasks import process_instagram_update

reactor = subscriptions.SubscriptionsReactor()

logger = logging.getLogger(__name__)


class InstagramPush(View):
    def get(self, request, subscription_pk, **kwargs):
        if 'hub.challenge' in request.GET:
            logger.debug('Got challenge verification request for '
                         'subscription {}'.format(subscription_pk))
        else:
            logger.debug('Got invalid GET request')

        return HttpResponse(request.GET.get('hub.challenge', 'error'))

    def post(self, request, subscription_pk, **kwargs):
        logger.debug('Got push request for subscription {}'.format(
            subscription_pk))
        x_hub_signature = request.META.get('HTTP_X_HUB_SIGNATURE')
        raw_response = request.body
        try:
            subscription = Subscription.objects.get(pk=subscription_pk)
            reactor.process(
                subscription.config['app_secret'],
                raw_response,
                x_hub_signature)
        except Exception:
            print 'Got error in reactor processing: %s' % raw_response
            exc_type, exc_value, exc_traceback = sys.exc_info()
            print exc_type, exc_value
        return HttpResponse('ok')


def process_update(update):
    process_instagram_update.s(update).apply_async()


reactor.register_callback(subscriptions.SubscriptionType.TAG,
                          process_update)
