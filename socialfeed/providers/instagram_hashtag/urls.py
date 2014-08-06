from django.conf.urls import url, patterns
from django.views.decorators.csrf import csrf_exempt

from .views import InstagramPush

urlpatterns = patterns(
    '',
    url(r'^push/(?P<subscription_pk>\d+)/$',
        csrf_exempt(InstagramPush.as_view()),
        name='instagram_verify_subscription'),
)
