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

    def save(self, *args, **kwargs):
        super(TrustItem, self).save(*args, **kwargs)

        if self.rating is not None:
            from trust.registry import apps, ModelNotRegistered

            try:
                trust_model = apps._registry[self.__class__]()
            except KeyError:
                model = self.__class__
                raise ModelNotRegistered("%s.%s is not registered." % (model._meta.app_label, model._meta.object_name))

            if self.rating >= 0:
                trust_model.trust(self)
            else:
                trust_model.deny(self)


class UserTrust(models.Model):
    user = models.OneToOneField("auth.User")
    verified = models.BooleanField(default=False)

    trust = models.IntegerField(blank=True, null=True, default=None, help_text="Allows you to set an exact Trust Level for Someone")
