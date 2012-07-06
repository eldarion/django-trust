from django.contrib import admin

from trust.models import TrustItem


class TrustItemAdmin(admin.ModelAdmin):
    raw_id_fields = ["user"]


admin.site.register(TrustItem, TrustItemAdmin)
