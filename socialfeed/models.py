from datetime import datetime
from importlib import import_module

from django.conf import settings
from django.db import models
from django.db.models.signals import post_save, pre_delete
from django.utils.translation import ugettext_lazy as _

from jsonfield import JSONField

PROVIDER_CHOICES = []
for provider_module in getattr(settings, 'SOCIALFEED_PROVIDERS'):
    module = import_module(provider_module)
    PROVIDER_CHOICES.append((provider_module, module.Provider.get_label()))


class Subscription(models.Model):
    is_active = models.BooleanField(_('is active'), default=False)
    title = models.CharField(_('title'), max_length=100)
    provider = models.CharField(
        _('provider'), max_length=100, choices=PROVIDER_CHOICES)
    subscription_id = models.CharField(
        _('subscription id'), max_length=100,
        help_text=_('provider related identifier of subscription'),
        blank=True, null=True)
    config = JSONField('config', blank=True)

    class Meta:
        verbose_name = _('subscription')
        verbose_name_plural = _('subscriptions')

    def __init__(self, *args, **kwargs):
        """
        Save the initial value of the is_active class for later use in the
        save method.
        """
        super(Subscription, self).__init__(*args, **kwargs)

        self.__initial_active_state = self.is_active

    def __unicode__(self):
        return self.title

    def save(self, *args, **kwargs):
        """
        Check if the is_active flag has changed and if so trigger the
        (un)subscribe methods on the provider.
        """
        if not self.__initial_active_state == self.is_active:
            if self.is_active:
                self.get_provider().subscribe()
            else:
                self.get_provider().unsubscribe()

        super(Subscription, self).save(*args, **kwargs)
        self.__initial_active_state = self.is_active

    @property
    def provider_class(self):
        module = import_module(self.provider)
        return module.Provider

    def get_provider(self):
        return self.provider_class(self)


def unsubscribe(sender, instance, **kwargs):
    instance.get_provider().unsubscribe()

pre_delete.connect(unsubscribe, sender=Subscription)


class PostManager(models.Manager):
    def active(self):
        return self.get_query_set().filter(is_active=True)


class Post(models.Model):
    is_active = models.BooleanField(_('is active'), default=True)
    subscription = models.ForeignKey(Subscription)
    source_id = models.CharField(_('source id'), max_length=100)
    created_at = models.DateTimeField(_('crated at'), null=True)
    data = JSONField('data')

    objects = PostManager()

    class Meta:
        unique_together = ('subscription', 'source_id')
        verbose_name = _('post')
        verbose_name_plural = _('posts')
        ordering = ['-created_at']
