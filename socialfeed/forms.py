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
                if field not in ['title', 'provider']:
                    self.fields.pop(field)
        else:
            config_fields = self.instance.provider_class.get_config_fields()
            for idx, config_field in enumerate(config_fields):
                try:
                    field_label, field_class, field_options = config_field
                except ValueError:
                    field_label, field_class = config_field
                    field_options = {}

                if not 'label' in field_options:
                    field_options['label'] = field_label.replace('_', ' ')

                field_name = 'config_var_{}'.format(idx)
                self.fields[field_name] = field_class(**field_options)
                self.fields[field_name].initial = self.instance.config.get(
                    field_label)

    def clean(self):
        super(SubscriptionAdminForm, self).clean()
        if self.instance.pk:
            provider = self.instance.get_provider()
            config_fields = provider.get_config_fields()
            for idx, config_field in enumerate(config_fields):
                field_name = 'config_var_{}'.format(idx)
                value = self.cleaned_data.get(field_name)
                self.instance.config[config_field[0]] = value
