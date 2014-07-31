=====
Trust
=====

Trust is a Django app for managing the trust levels of your users. All users
start out with a default amount of trust, and as they do good things they gain
trust, and as they do bad things they lose trust.

Whenever users create new content on the site it can be placed into the trust
queue. Trust will then look at a users trust, and the context that this content
is in and decide if this user should be automatically trusted, moderated until
a staff member can rate the post, or automatically rejected as being untrustworthy.

This project is brought to you by Midwest Communications.


Development
-----------

The source repository can be found at https://github.com/eldarion/django-trust


Contents
========

.. toctree::
 :maxdepth: 1

 changelog
 installation
 templatetags
 signals
 usage
