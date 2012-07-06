from django.conf.urls.defaults import *

from trust.views import TrustQueue, RateView

urlpatterns = patterns("",
    url(r"^manage/", include(patterns("",
        url(r"^queue/$", TrustQueue.as_view(), name="manage_trust_queue"),
        url(r"^rate/(?P<pk>\d+)/$", RateView.as_view(), name="rate_trust_item"),
    ))),
)
