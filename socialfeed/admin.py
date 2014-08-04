from django.contrib import admin
from django.utils.safestring import mark_safe

from . import models
from . import forms


class SubscriptionAdmin(admin.ModelAdmin):
    form = forms.SubscriptionAdminForm
    list_display = ['title', 'provider', 'is_active']
    readonly_fields = ['subscription_id', 'config']

    def get_fields(self, request, obj=None):
        if not obj:
            return ['provider']
        else:
            return super(SubscriptionAdmin, self).get_fields(request, obj)

    def get_fieldsets(self, request, obj=None):
        fieldsets = super(SubscriptionAdmin, self).get_fieldsets(request, obj)

        if obj:
            for field in fieldsets[0][1]['fields'][:]:
                if field[:10] == 'config_var':
                    fieldsets[0][1]['fields'].remove(field)

            config_var_names = obj.get_provider().get_config_fields()
            config_fields = ['config_var_{}'.format(idx) for idx
                             in range(0, len(config_var_names))]
            fieldsets.append(('config', {'fields': config_fields}))

        return fieldsets


class PostAdmin(admin.ModelAdmin):
    list_display = ['admin_thumbnail', 'admin_title', 'created_at', 'provider']
    list_filter = ['subscription']

    def provider(self, instance):
        return instance.subscription.provider

    def admin_thumbnail(self, instance):
        provider = instance.subscription.get_provider()
        url = provider.get_post_thumbnail(instance)
        if url:
            return mark_safe(
                u'<img src="{}" width="75" alt="" />'.format(url))
        else:
            return None

    def admin_title(self, instance):
        title = instance.subscription.get_provider().get_post_title(instance)
        return title


admin.site.register(models.Subscription, SubscriptionAdmin)
admin.site.register(models.Post, PostAdmin)
