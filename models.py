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

    @property
    def provider_class(self):
        module = import_module(self.provider)
        return module.Provider

    def get_provider(self):
        return self.provider_class(self)


def subscribe(sender, instance, **kwargs):
    if instance.is_active and not 'subscription_id' in instance.config:
        provider = instance.get_provider()
        provider.subscribe()


def unsubscribe(sender, instance, **kwargs):
    if not instance.is_active and 'subscription_id' in instance.config:
        provider = instance.get_provider()
        provider.unsubscribe()

post_save.connect(subscribe, sender=Subscription)
pre_delete.connect(unsubscribe, sender=Subscription)


class Post(models.Model):
    is_active = models.BooleanField(_('is active'), default=True)
    subscription = models.ForeignKey(Subscription)
    source_id = models.CharField(_('source id'), max_length=100)
    data = JSONField('data')

    class Meta:
        unique_together = ('subscription', 'source_id')
        verbose_name = _('post')
        verbose_name_plural = _('posts')
