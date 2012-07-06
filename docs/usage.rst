.. _usage:

Usage
=====

In order to use Trust with a model you must create a TrustApp, these are
subclasses of ``trust.registry.TrustApp`` and they encapsulate the logic
that should happen at various states of trust.

An example trust app might be::

    class CommentTrust(TrustApp):

        def trust(self, obj, user=None):
            # This will be called if the user is trusted for this object.
            # You can use it to publish a post, unhide a comment, or any other
            # action that should happen when your object is trusted.
            obj.hidden = False
            obj.save()

        def moderate(self, obj, user=None):
            # This will be called if the user is not trusted for this object,
            # but they are not untrusted. We don't know so they have been placed
            # in a queue to wait for staff approval. You can use it to hide a
            # post, mark it as moderated, or any other action that should happen
            # when your object has been moderated.
            obj.hidden = True
            obj.save()

        def deny(self, obj, user=None):
            # This will be called if the user is untrusted for this object.
            # You can use it to delete the object, or whatever action would
            # be appropriate for when the object has been denied.
            obj.delete()

Taking the above trust app, you could then register it by doing::

    from trust.registry import apps

    apps.register(Comment, CommentTrust)  # Where Comment is a Django model


Once you have you TrustApp and you've registered it then you can begin to use it.
This is fairly simple as well. There are 2 major methods that will be useful.

The first is ``is_trusted`` which is used to determine if a user is trusted
for a certain context or not. It's usage is simple::

    from trust.registry import apps

    apps.is_trusted(USER)  # Returns True/False/None based on if the user is trusted in the default context
    apps.is_trusted(USER, context="comments")  # The same as above, but for the comments context

The return values are ``True`` if the user should be trusted, ``None`` if we
don't know if the user should be trusted (and thus they should be moderated), and
``False`` if the user should not be trusted.

The second method is ``moderate`` which is used to pass an object into the Trust
system. To use it simply::

    from trust.registry import apps

    # Place OBJ by USER into the trust system calling the appropriate TrustApp
    #   methods based on trust level.
    apps.moderate(USER, OBJ)

    # Place OBJ by USER in comments context into the trust system calling the
    #   appropriate TrustApp methods based on trust level.
    apps.moderate(USER, OBJ, context="comments")


Contexts
~~~~~~~~

In Trust, a context is a unique string that is used to seperate out different
sections or sets of content. They are most useful for when you want different
levels of required trust for different types of things. For instance it might
require a trust level of 3 to post a comment, but a trust level of 8 to post blog
posts.

Contexts are implemented as simple model that contains ``name``, ``trusted_level``,
and ``moderated_level``. ``name`` is used as the unique string that identifies
a context. ``trusted_level`` and ``moderated_level`` are the minimum amount of
trust a user is required to have to be trusted or moderated in this context.

If you pass in an invalid context to any of the methods in trust, it will fail
silently and use the default trust values. This allows you to scope your contexts
early without having to define a context or levels for each one.
