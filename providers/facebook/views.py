import urllib
from urlparse import parse_qs

from django.contrib.sites.models import Site
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import View, FormView
from django.views.generic.detail import SingleObjectMixin

from socialfeed.models import Subscription
from facepy import GraphAPI

from .forms import RequestAccessTokenForm


class RequestAccessTokenView(FormView):
    template_name = 'socialfeed/facebook/request_access_token.html'
    form_class = RequestAccessTokenForm

    def form_valid(self, form):
        subscription = form.cleaned_data['subscription']
        app_id = subscription.config['app_id']
        redirect_uri = 'http://{}{}'.format(
            Site.objects.get_current().domain,
            reverse('facebook_authorize_access_token', kwargs={
                'pk': subscription.pk
            }))

        params = urllib.urlencode({
            'client_id': app_id,
            'redirect_uri': redirect_uri,
            'scope': 'read_stream,user_photos'
        })
        url = 'http://www.facebook.com/dialog/oauth?{}'.format(params)

        return HttpResponseRedirect(url)


class AuthorizeAccessTokenView(SingleObjectMixin, View):
    model = Subscription

    def get(self, request, *args, **kwargs):
        code = request.GET.get('code')

        subscription = self.get_object()

        redirect_uri = 'http://{}{}'.format(
            Site.objects.get_current().domain
            reverse('facebook_authorize_access_token', kwargs={
                'pk': subscription.pk
            }))

        graph = GraphAPI()
        response = graph.get(
            path='oauth/access_token',
            client_id=subscription.config['app_id'],
            client_secret=subscription.config['app_secret'],
            redirect_uri=redirect_uri,
            code=code)

        data = parse_qs(response)

        subscription.config['access_token'] = data['access_token'][0]
        subscription.config['access_token_expiration_date'] = data['expires'][0]
        subscription.save()

        return HttpResponse('worked')


class FacebookPushView(View):
    def get(self, request, *args, **kwargs):
        return HttpResponse(request.GET.get('hub.challenge'))

    def post(self, request, *args, **kwargs):
        print '---'
        print request.body
        print '==='
