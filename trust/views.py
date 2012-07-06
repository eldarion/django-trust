from django.core.urlresolvers import reverse_lazy
from django.views.generic import ListView, UpdateView

from trust.models import TrustItem
from trust.forms import RateForm


class TrustQueue(ListView):
    queryset = TrustItem.objects.filter(rating=None)


class RateView(UpdateView):
    model = TrustItem
    form_class = RateForm
    success_url = reverse_lazy("manage_trust_queue")
