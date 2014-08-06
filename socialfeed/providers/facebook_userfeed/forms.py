from django import forms

from socialfeed.models import Subscription


class RequestAccessTokenForm(forms.Form):
    subscription = forms.ModelChoiceField(queryset=Subscription.objects.all())

    def form_valid(self, form):
        form.cleaned_data.get('subscription').data['app_id']
