from django.contrib import admin

from . import models
from . import forms


class SubscriptionAdmin(admin.ModelAdmin):
    form = forms.SubscriptionAdminForm
    readonly_fields = ['config']

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

            config_var_names = obj.get_provider().config_fields
            config_fields = ['config_var_{}'.format(idx) for idx
                             in range(0, len(config_var_names))]
            fieldsets.append(('config', {'fields': config_fields}))

        return fieldsets


class PostAdmin(admin.ModelAdmin):
    pass


admin.site.register(models.Subscription, SubscriptionAdmin)
admin.site.register(models.Post, PostAdmin)
