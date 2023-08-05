import logging
from urllib.parse import unquote
import warnings

from django.conf import settings
from django.contrib.auth.middleware import RemoteUserMiddleware

from .errors import EmptySandstormPermissionsHeaderWarning

logger = logging.getLogger(__name__)


class DLSMiddleware(RemoteUserMiddleware):

    header = "HTTP_X_SANDSTORM_USER_ID"

    def process_request(self, request):
        super().process_request(request)

        request.user.name = unquote(
            request.META.get("HTTP_X_SANDSTORM_USERNAME", "Anonymous%20User")
        )
        request.user.handle = request.META.get(
            "HTTP_X_SANDSTORM_PREFERRED_HANDLE", "anonymous"
        )
        if request.user.is_authenticated:
            request.user.save()

        permissions_header = request.META.get(
            "HTTP_X_SANDSTORM_PERMISSIONS", ""
        )
        if len(permissions_header) == 0:
            warnings.warn(EmptySandstormPermissionsHeaderWarning())
            logger.warn(
                "Received no permissions from Sandstorm.  Have you configured permissions in sandstorm-pkgdef.capnp?"
            )
            sandstorm_permissions = set()
        else:
            sandstorm_permissions = set(permissions_header.split(","))
        if (
            hasattr(settings, "DLS_SUPERUSER_PERMISSION")
            and settings.DLS_SUPERUSER_PERMISSION in sandstorm_permissions
        ):
            request.user.is_superuser = True
            sandstorm_permissions.remove(settings.DLS_SUPERUSER_PERMISSION)
        else:
            request.user.is_superuser = False
        if (
            hasattr(settings, "DLS_STAFF_PERMISSION")
            and settings.DLS_STAFF_PERMISSION in sandstorm_permissions
        ):
            request.user.is_staff = True
            sandstorm_permissions.remove(settings.DLS_STAFF_PERMISSION)
        else:
            request.user.is_staff = False
        if hasattr(
            request.user, "set_permissions_from_sandstorm"
        ) and callable(request.user.set_permissions_from_sandstorm):
            request.user.set_permissions_from_sandstorm(sandstorm_permissions)
