from django.core.urlresolvers import reverse_lazy
from django.views.generic import ListView, UpdateView
from django.utils.decorators import method_decorator

from django.contrib.admin.views.decorators import staff_member_required

from trust.models import TrustItem
from trust.forms import RateForm


class TrustQueue(ListView):
    queryset = TrustItem.objects.filter(rating=None)

    @method_decorator(staff_member_required)
    def dispatch(self, *args, **kwargs):
        return super(TrustQueue, self).dispatch(*args, **kwargs)


class RateView(UpdateView):
    model = TrustItem
    form_class = RateForm
    success_url = reverse_lazy("manage_trust_queue")

    @method_decorator(staff_member_required)
    def dispatch(self, *args, **kwargs):
        return super(RateView, self).dispatch(*args, **kwargs)
