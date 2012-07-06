from django.conf import settings
from django.db.models import Avg

from django.contrib.contenttypes.models import ContentType

from trust.models import TrustContext, UserTrust, TrustItem


class ModelAlreadyRegistered(Exception):
    pass


class ModelNotRegistered(Exception):
    pass


class TrustApp(object):

    def trust(self, obj, user=None):
        raise NotImplementedError("trust not implemented")

    def moderate(self, obj, user=None):
        raise NotImplementedError("moderate not implemented")

    def deny(self, obj, user=None):
        raise NotImplementedError("deny not implemented")


class TrustAppRegistry(object):

    def __init__(self):
        self._registry = {}

    def register(self, model, trust_app):
        if model in self._registry:
            raise ModelAlreadyRegistered("%s.%s is already registered." % (model._meta.app_label, model._meta.object_name))

        self._registery[model] = trust_app

    def unregister(self, model):
        if not model in self._registry:
            raise ModelNotRegistered("%s.%s is not registered." % (model._meta.app_label, model._meta.object_name))

    def is_trusted(self, user, context=None):
        """
        Returns True if a user can be trusted, False if they must not be trusted, and
        None if we do not know if they can be trusted. It can optionally take a context,
        a context is a string that will be used to fetch the proper thresholds instead of
        using the default.

        The return values will typically be mapped as so:
           True  - Auto Allow Action
           None  - Allow Action, but Require Moderator Approval
           False - Disallow Action
        """

        if not user.is_authenticated():
            # Anonymous users are always untrusted
            return False

        if user.is_staff:
            # Staff users are always trusted
            return True

        if context is not None:
            ctx = next(iter(TrustContext.objects.filter(name=context)[:1]), None)
        else:
            ctx = None

        if ctx is None:
            moderated_level = settings.TRUST_DEFAULT_MODERATED_LEVEL
            trusted_level = settings.TRUST_DEFAULT_TRUST_LEVEL
        else:
            moderated_level = ctx.moderated_level
            trusted_level = ctx.trusted_level

        ut = UserTrust.objects.get_or_create(user=user)

        # If a User has hard coded trust, use those values
        if ut.trust is not None:
            if trusted_level is not None and ut.trust >= trusted_level:
                return True
            elif moderated_level is not None and ut.trust >= moderated_level:
                return  None
            else:
                return False

        # Get Aggregated Trust for User
        trust = TrustItem.objects.filter(user=user, rating__isnull=False).aggregate(trust=Avg("rating")).get("trust", settings.DEFAULT_TRUST_LEVEL)

        if trusted_level is not None and trust >= trusted_level:
            return True
        elif moderated_level is not None and trust >= moderated_level:
            return None
        else:
            return False

    def moderate(self, user, obj, context=None):
        trusted = self.is_trusted(user, context=context)

        try:
            trust_model = self._registry[obj.__class__]()
        except KeyError:
            model = obj.__class__
            raise ModelNotRegistered("%s.%s is not registered." % (model._meta.app_label, model._meta.object_name))

        if trusted:
            trust_model.trust(obj, user)
        elif trusted is None:
            trust_model.moderate(obj, user)
        else:
            trust_model.deny(obj, user)

        TrustItem.objects.create(
                            content_type=ContentType.objects.get_for_model(TrustItem),
                            object_id=obj.pk,
                            user=user,
                            rating=None
                        )


apps = TrustAppRegistry()
