.. _overview:

Usage overview
==============

The goal of django-soapbox is to provide a way to display persistent
messages on either all pages, specific pages, or a subset of pages on
a Django-powered site. To begin using django-soapbox, :ref:`install it
<install>`, then add `soapbox` to your `INSTALLED_APPS` setting
and run `manage.py migrate` to install the :class:`Message` model.

You can then begin creating :class:`Message` instances through the
admin interface, indicating which URLs you'd like them to appear on.


Provided models
---------------

.. currentmodule:: soapbox.models

.. class:: Message

   The core of django-soapbox is the :class:`Message` model, which
   represents messages to be displayed on your site. This model has
   four fields and one important custom method:

   .. attribute:: message

       A :class:`~django.db.models.TextField` containing the text of
       the message to display. This can be plain text, or can include
       HTML.

   .. attribute:: is_active

       A :class:`~django.db.models.BooleanField` (defaults to :data:`True`)
       indicating whether the message is currently active; only active
       messages will be retrieved by the standard helpers built in to
       django-soapbox.

   .. attribute:: is_global

       A :class:`~django.db.models.BooleanField` (defaults to
       :data:`False`) indicating whether the message is global; a
       global message does not need to have :attr:`url` (see below)
       set, and will match any URL.

   .. attribute:: url

       A :class:`~django.db.models.CharField` to optionally indicate
       the URL(s) on your site with which this message should be
       associated. Not needed if :attr:`is_global` is :data:`True`.

   .. method:: match(url)

       Return :data:`True` if this `Message` matches `url`, `False`
       otherwise. If `is_global` is :data:`True`, will always return
       :data:`True`.

       :param str url: The URL to check against.
       :rtype: bool


.. class:: MessageManager

   Also provided on :class:`Message` is a custom manager, accessible as
   the attribute :attr:`~Message.objects`, which defines two useful methods:

   .. method:: active()

       Returns a :class:`~django.db.models.QuerySet` of all
       :class:`Message` instances which have
       :attr:`~Message.is_active` set to :data:`True`. This is defined
       as a custom :class:`~django.db.models.QuerySet` method, so it
       can also be "chained" with other
       :class:`~django.db.models.QuerySet` methods. For example, the
       following would retrieve all :class:`Message` instances which
       are both global and active:

       .. code-block:: python

           Message.objects.filter(is_global=True).active()

       :rtype: :class:`~django.db.models.QuerySet`

   .. method:: match(url)

       Return a list -- *not* a :class:`~django.db..models.QuerySet` -- of
       all :class:`Message` instances which match `url`.

       :rtype: list


Validation requirements
-----------------------

While :class:`Message` instances are relatively freeform, there are
two requirements you must abide by; failure to do so will result in
validation errors being raised when trying to save the
:class:`Message`:

1. Each :class:`Message` must either have :attr:`~Message.is_global`
   set to :data:`True`, or specify some URL prefix to match in
   :attr:`~Message.url`.

2. A :class:`Message` cannot have both :attr:`~Message.is_global` set
   to :data:`True` and simultaneously have a URL prefix to match
   specified in :attr:`~Message.url` (in other words, a
   :class:`Message` can be global, or "local" to some URL prefix, but
   never both at the same time).


Message URL matching
--------------------

The message-retrieval helpers provided in django-soapbox will only
retrieve messages which are active and which match a particular URL
you pass to them; typically, this will be the URL of the current
request. The matching process is case-sensitive and uses the following
algorithm, implemented in the :meth:`~Message.match()` method of
:class:`Message`.

1. If the :class:`Message` has `is_global` set to :data:`True`,
   immediately return :data:`True`.

2. Strip leading and trailing slashes from the URL, and from the
   :attr:`~Message.url` field of the :class:`Message`, and split each
   on internal slashes to yield a list of path components.

3. If the list of components from the :attr:`~Message.url` field of
   the :class:`Message` is longer than the list from the passed-in
   URL, immediately return :data:`False`.

4. Return :data:`True` if the list of components from the
   :attr:`~Message.url` field, and the corresponding list of
   components from the beginning of the passed-in URL, are
   equal. Otherwise, return :data:`False`.

This means that a :class:`Message` will match not only a URL which is
an exact match for its own :attr:`~Message.url`, but also any URL of
which its :attr:`~Message.url` is a prefix. So, for example, if the
:attr:`~Message.url` field contained `/foo/`, it would match on
`/foo/` *and* on `/foo/bar/`.


Retrieving and displaying messages
----------------------------------

There are two helpers built in to django-soapbox for retrieving and
displaying messages in templates.

One is a context processor, which will add a variable
`soapbox_messages` to the context of any template rendered with a
:class:`~django.template.RequestContext` (required in order to have
access to the request path to determine the URL). To enable it, add
`soapbox.context_processors.soapbox_messages` to the context
processors enabled on your site. See `the Django template options
documentation
<https://docs.djangoproject.com/en/stable/topics/templates/#django.template.backends.django.DjangoTemplates>`_
for notes on how to do this.

If you prefer to have more fine-grained control of where messages will
be retrieved and displayed, django-soapbox provides a template tag,
`get_soapbox_messages` which can retrieve messages for a given URL
and place them into a variable in the context. The syntax of the tag
is:

.. code-block:: django

    {% get_messages_for_page [url] as [varname] %}

To use the tag, first add `{% load soapbox %}` to the template to
load the django-soapbox template tag library, then call the
`get_messages_for_page` tag, passing a URL -- either a string, or a
template variable which the tag will resolve -- and the name of the
context variable you'd like the message to be placed into. For example
(presuming you have a context processor enabled which exposes the
current HTTP request to your template):

.. code-block:: django

    {% load soapbox %}
    {% get_messages_for_page request.path as soapbox_messages %}

    {% for message in soapbox_messages %}
      <p>Important message: {{ message }}</p>
    {% endfor %}


What django-soapbox is not
--------------------------

Importantly, django-soapbox is not a system for displaying one-time
"flash"-type notifications to an individual user; for that, use
`Django's built-in message framework
<https://docs.djangoproject.com/en/stable/ref/contrib/messages/>`_. It
also is not a system for users to send messages to each other; for
that, email or a custom user-message tool is more appropriate.

Instead, django-soapbox is for displaying messages to *all* users, on
any URLs the messages match, each time they visit those URLs. Most
often this is useful for site-wide or section-specific announcements
all users need to see.


Security considerations
-----------------------

The tools provided in django-soapbox are designed around the
assumption that only trusted administrators of your site will be
permitted to create :class:`Message` instances. In particular, a
:class:`Message` will, by default, mark its contents as safe for display,
and so the Django template system will *not* perform autoescaping of
the contents. This is useful for allowing HTML messages -- for
example, containing links to longer announcements on their own pages
-- but if opened to arbitrary or untrusted users would be a serious
`cross-site scripting vulnerability
<http://en.wikipedia.org/wiki/Cross-site_scripting>`_

Because of this, it is recommended that you only use the Django
administrative interface to create `Message` instances, and that you
carefully restrict the `soapbox.add_message` permission to only a
small number of trusted administrators.