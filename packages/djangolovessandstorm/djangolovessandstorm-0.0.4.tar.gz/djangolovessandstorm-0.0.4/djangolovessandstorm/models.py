import logging
from typing import List

from django.db import models
from django.utils.crypto import salted_hmac
from django.utils.translation import gettext as _

STAR_PREFIXES = frozenset(["add", "change", "delete", "view"])

logger = logging.getLogger(__name__)


class SandstormUser(models.Model):
    id = models.CharField(
        primary_key=True,
        max_length=32,
        verbose_name=_("Sandstorm User ID"),
    )  # type: models.CharField
    handle = models.CharField(
        max_length=200,
        verbose_name=_("handle"),
    )  # type: models.CharField
    name = models.CharField(
        max_length=200,
        verbose_name=_("name"),
    )  # type: models.CharField
    email = models.EmailField(blank=True)  # type: models.EmailField
    session_key = models.CharField(
        max_length=64,
        verbose_name=_("session key"),
    )  # type: models.CharField

    # username here is a pseudorandom 32-bit value
    USERNAME_FIELD = "id"
    # Many Django applications expect to be able to store an e-mail address.
    EMAIL_FIELD = "email"
    REQUIRED_FIELDS = []  # type: List[str]

    # Will always be able to login.  Sandstorm controls this.
    @property
    def is_active(self):
        return True

    # RemoteUserMiddleware will not instantiate this model if the user is
    # anonymous.
    @property
    def is_anonymous(self):
        return False

    @property
    def is_authenticated(self):
        return True

    @classmethod
    def get_email_field_name(klass):
        # It is not required that Sandstorm users have e-mail addresses, but
        # many Django applications expect one.
        return klass.EMAIL_FIELD

    def get_full_name(self):
        return self.name

    def get_short_name(self):
        return self.name

    # Sandstorm usernames are pseudorandom 32-bit hex-encoded values
    def get_username(self):
        return self.id

    @classmethod
    def normalize_username(klass, username):
        raise NotImplementedError(
            "SandstormUsers do not have normal usernames"
        )

    # Passwords

    def check_password(self, password):
        raise NotImplementedError("SandstormUsers do not have passwords")

    def has_usable_password(self):
        return False

    def set_password(self, password):
        raise NotImplementedError("SandstormUsers do not have passwords")

    def set_unusable_password(self, password):
        raise NotImplementedError("SandstormUsers do not have passwords")

    # Session hash

    def get_session_auth_hash(self):
        "Return an HMAC of a random value for the session key"
        key_salt = (
            "djangolovessandstorm.models.SandstormUser.get_session_auth_hash"
        )
        return salted_hmac(key_salt, self.session_key).hexdigest()

    # Permissions

    def has_module_perms(self, app_label):
        has_module_perms_result = self._has_module_perms(app_label)
        result = self.is_superuser or has_module_perms_result
        logger.debug(
            "{} has_module_perms {}: superuser={} granted={} -> {}".format(
                self.name,
                app_label,
                self.is_superuser,
                has_module_perms_result,
                result,
            )
        )
        return result

    def has_perm(self, permission, obj=None):
        has_perm_result = self._has_perm(permission, obj)
        result = self.is_superuser or has_perm_result
        logger.debug(
            "{} has_perm permission={}: superuser={} granted={} -> {}".format(
                self.name,
                permission,
                self.is_superuser,
                has_perm_result,
                result,
            )
        )
        return result

    def _has_module_perms(self, app_label):
        return (
            hasattr(self, "_module_perms") and app_label in self._module_perms
        )

    def _has_perm(self, permission, obj):
        return (
            hasattr(self, "_permissions") and permission in self._permissions
        )

    def set_permissions_from_sandstorm(self, sandstorm_permissions):
        if hasattr(self, "_module_perms") or hasattr(self, "_permissions"):
            raise RuntimeError(
                "Call set_permissions_from_sandstorm only once per request"
            )
        self._module_perms = set()
        self._permissions = set()
        for permission in sandstorm_permissions:
            if "." in permission:
                module, _ = permission.split(".", 1)
                self._module_perms.add(module)
                if "*" in permission:
                    for starprefix in STAR_PREFIXES:
                        self._permissions.add(
                            permission.replace("*", starprefix, 1)
                        )
                self._permissions.add(permission)
            else:
                logger.warn(
                    "Received permission without an app label: {0!r}".format(
                        permission
                    )
                )
        logger.debug(
            "Set permissions from Sandstorm: {!r}".format(self._permissions)
        )

    def __str__(self):
        return self.name
