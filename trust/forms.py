from django import forms

from trust.models import TrustItem


class RateForm(forms.ModelForm):
    class Meta:
        model = TrustItem
        fields = ["rating"]

    def save(self, *args, **kwargs):
        commit = kwargs.get("commit", True)
        kwargs["commit"] = False

        obj = super(RateForm, self).save(*args, **kwargs)
        obj.queued = False

        if commit:
            obj.save()

        return obj
