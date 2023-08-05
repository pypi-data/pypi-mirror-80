======================
Django Loves Sandstorm
======================

Django Loves Sandstorm (D♥S, ``DLS…`` and ``djangolovessandstorm``) provides
tools for adapting Django applications to work with Sandstorm.  For
authentication, D♥S uses `HTTP headers provided by Sandstorm`_ to manage
``SandstormUser`` objects as required by `Django Auth`_.

.. _`HTTP headers provided by Sandstorm`: https://docs.sandstorm.io/en/latest/developing/auth/#headers-that-an-app-receives
.. _`Django Auth`: https://docs.djangoproject.com/en/2.2/topics/auth/

Installation and Configuration
==============================

D♥S requires installation in your Python environment and configuration in your
Django project.  This section documents the required configuration.

Apps
----

If using the suggested ``SandstormUser`` user model, the
``djangolovessandstorm`` app must be added to the Django ``INSTALLED_APPS``
list::

    INSTALLED_APPS = [
        …
        "djangolovessandstorm.apps.DLSConfig",
        …
    ]

Authentication Backends
-----------------------

D♥S provides the ``DLSAllowAllUsersBackend`` authentication backend, which
populates the ``SandstormUser`` model from the HTTP headers
provided by the Sandstorm HTTP bridge.  Use it by adding it to the
``AUTHENTICATION_BACKENDS`` list in the Django settings::

    AUTHENTICATION_BACKENDS = [
        "djangolovessandstorm.backends.DLSAllowAllUsersBackend",
    ]

Authentication Model
--------------------

D♥S suggests the use of the ``SandstormUser`` model.  Set the
``AUTH_USER_MODEL`` in Django settings::

    AUTH_USER_MODEL = "djangolovessandstorm.SandstormUser"

Middleware
----------

D♥S requires the use of middleware to read these HTTP headers and create the
appropriate ``SandstormUser`` objects.  This middleware is found in the
``djangolovessandstorm.middleware`` module.

It is added to the Django settings ``MIDDLEWARE`` list.  In the list of
middleware, ``SessionMiddleware`` should appear before
``AuthenticationMiddleware``.  ``AuthenticationMiddleware`` should appear
before ``DLSMiddleware``::

    MIDDLEWARE = [
        …
        "django.contrib.sessions.middleware.SessionMiddleware",
        "
        …
        "django.contrib.auth.middleware.AuthenticationMiddleware",
        …
        "djangolovessandstorm.middleware.DLSMiddleware",
        …
    ]

Permissions
-----------

To use the Django Auth superuser and staff roles, configure the
corresponding permissions in the Django settings.  D♥S will look for these
permissions in the ``X-Sandstorm-Permissions`` HTTP header, which will
appear based upon the settings of ``bridgeConfig.viewInfo.permissions``
inside ``sandstorm-pkgdef.capnp``.  For example, the following two lines in
your Django settings, will result in Django expecting ``superuser`` and
``staff`` to be set in ``sandstorm-pkgdef.capnp``::

    DLS_SUPERUSER_PERMISSION = "superuser"
    DLS_STAFF_PERMISSION = "staff"

To make this work, ``superuser`` and ``staff`` should be named as
permissions in ``sandstorm-pkgdef.capnp``::

    bridgeConfig = (
      viewInfo = (
        permissions = [
          (
            name = "superuser",
            title = (defaultText = "superuser"),
            description = (defaultText = "full control"),
          ),
          (
            name = "staff",
            title = (defaultText = "staff"),
            description = (defaultText = "administrator interface access"),
          ),
        ],
        roles = [
          (
            title = (defaultText = "Full access"),
            permissions = [
              true,  # superuser
              true,  # staff
            ],
            verbPhrase = (defaultText = "full access"),
            description = (defaultText = "may view and alter all data and settings"),
          ),
          (
            title = (defaultText = "Staff"),
            permissions = [
              false, # superuser
              true,  # staff
            ],
            verbPhrase = (defaultText = "staff may administer some applications"),
            description = (defaultText = "may view and alter all some data and settings through Django Admin"),
          ),
        ],
      ),
    ),

How It Works
============

D♥S middleware processes requests, creating and updating ``SandstormUser``
objects as necessary.  To understand how the code works, look first at the
middleware.

``DLSMiddleware`` inherits from
``django.contrib.auth.middleware.RemoteUserMiddleware``.  To understand the
code, begin by reading the ``process_request`` method.

``DLSMiddleware.process_request`` calls
``RemoteUserMiddleware.process_request``, which performs some sanity checks
before calling ``django.contrib.auth.authenticate`` and
``django.contrib.auth.login``.  If the authentication backend does not find the
user in the database, a new user is ``create``d, ``save``d and configured
(``configure_user``).  ``DLSAllowAllUsersBackend.configure_user`` stores the
userʼs name and handle, and generates a session key.  (The session key is
necessary because a SandstormUser does not have a password hash, which would
otherwise function as the session key.)
