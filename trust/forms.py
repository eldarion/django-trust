from django import forms

from trust.models import TrustItem


class RateForm(forms.ModelForm):
    class Meta:
        model = TrustItem
        fields = ["rating"]
