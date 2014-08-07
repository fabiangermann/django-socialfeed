from django.conf.urls import url, patterns

from .views import RequestAccessTokenView, RedeemAccessTokenView

urlpatterns = patterns(
    '',
    url(r'^request-access-token/$',
        RequestAccessTokenView.as_view(),
        name='facebook_request_access_token'),
    url(r'^(?P<pk>\d+)/redeem-access-token/$',
        RedeemAccessTokenView.as_view(),
        name='facebook_redeem_access_token'),
)
