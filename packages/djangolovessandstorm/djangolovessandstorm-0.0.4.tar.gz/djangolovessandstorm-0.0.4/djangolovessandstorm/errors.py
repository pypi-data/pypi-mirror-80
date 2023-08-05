class DLSWarning(UserWarning):
    """Warnings for Django Loves Sandstorm"""


class EmptySandstormPermissionsHeaderWarning(DLSWarning):
    """
    Empty ``X-Sandstorm-Permissions`` header

    When no permissions are configured in the
    ``bridgeConfig.viewInfo.permissions`` of sandstorm-pkgdef.capnp, the
    ``X-Sandstorm-Permissions`` header is empty.  This warning reminds the
    developer to configure permissions.
    """

    def __str__(self):
        return "X-Sandstorm-Permissions header is empty"
