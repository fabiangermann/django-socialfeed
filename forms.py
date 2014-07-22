from django import forms
from django.utils.translation import ugettext_lazy as _


class SubscriptionAdminForm(forms.ModelForm):
    config_var_0 = forms.CharField(
        label=_('config variable 0'), required=False)
    config_var_1 = forms.CharField(
        label=_('config variable 1'), required=False)
    config_var_2 = forms.CharField(
        label=_('config variable 2'), required=False)
    config_var_3 = forms.CharField(
        label=_('config variable 3'), required=False)
    config_var_4 = forms.CharField(
        label=_('config variable 4'), required=False)
    config_var_5 = forms.CharField(
        label=_('config variable 5'), required=False)
    config_var_6 = forms.CharField(
        label=_('config variable 6'), required=False)
    config_var_7 = forms.CharField(
        label=_('config variable 7'), required=False)
    config_var_8 = forms.CharField(
        label=_('config variable 8'), required=False)
    config_var_9 = forms.CharField(
        label=_('config variable 9'), required=False)

    def __init__(self, *args, **kwargs):
        super(SubscriptionAdminForm, self).__init__(*args, **kwargs)

        if not self.instance.pk:
            for field in self.fields.copy():
                if not field == 'provider':
                    self.fields.pop(field)
        else:
            config_fields = self.instance.provider_class.get_config_fields()
            for idx, config_var_name in enumerate(config_fields):
                field = self.fields['config_var_{}'.format(idx)]
                field.label = config_var_name.replace('_', ' ')
                field.required = True
                field.initial = self.instance.config.get(config_var_name)

    def clean(self):
        super(SubscriptionAdminForm, self).clean()
        if self.instance.pk:
            provider = self.instance.get_provider()
            for idx, config_var_name in enumerate(provider.get_config_fields()):
                field_name = 'config_var_{}'.format(idx)
                value = self.cleaned_data.get(field_name)
                self.instance.config[config_var_name] = value
