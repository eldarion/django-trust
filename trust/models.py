from django.db import models

from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic


class TrustContext(models.Model):
    name = models.SlugField(max_length=25, unique=True)
    trusted_level = models.IntegerField(blank=True, null=True, help_text="The minimum trust level a user must be to be automatically trusted.")
    moderated_level = models.IntegerField(blank=True, null=True, help_text="The minimum trust level a user must be to be allowed, but moderated.")


class TrustItem(models.Model):
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = generic.GenericForeignKey('content_type', 'object_id')

    user = models.ForeignKey("auth.User")
    rating = models.IntegerField(null=True, default=None)


class UserTrust(models.Model):
    user = models.OneToOneField("auth.User")
    verified = models.BooleanField(default=False)

    trust = models.IntegerField(blank=True, null=True, default=None, help_text="Allows you to set an exact Trust Level for Someone")
