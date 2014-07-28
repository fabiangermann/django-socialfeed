from django.core.management.base import BaseCommand

from socialfeed.models import Subscription

class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        subscriptions = Subscription.objects.filter(is_active=True)

        for subscription in subscriptions:
            subscription.get_provider().pull_posts()
