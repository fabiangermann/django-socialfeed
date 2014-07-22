from django.conf.urls import url, patterns
from django.views.decorators.csrf import csrf_exempt

from .views import (RequestAccessTokenView, AuthorizeAccessTokenView,
                    FacebookPushView)

urlpatterns = patterns(
    '',
    url(r'^request-access-token/$',
        RequestAccessTokenView.as_view(),
        name='facebook_request_access_token'),
    url(r'^(?P<pk>\d+)/authorize-access-token/$',
        AuthorizeAccessTokenView.as_view(),
        name='facebook_authorize_access_token'),
    url(r'push/$',
        csrf_exempt(FacebookPushView.as_view()),
        name='socialfeed_facebook_push'),
)


