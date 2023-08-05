from urllib.parse import unquote

from django.contrib.auth.backends import AllowAllUsersRemoteUserBackend
from django.utils.crypto import get_random_string


class DLSAllowAllUsersBackend(AllowAllUsersRemoteUserBackend):

    # configure_user is called once, when the user is created.
    def configure_user(self, request, user):
        user.name = unquote(request.META.get("HTTP_X_SANDSTORM_USERNAME"))
        user.handle = request.META.get("HTTP_X_SANDSTORM_PREFERRED_HANDLE")
        session_key_length = user._meta.get_field("session_key").max_length
        user.session_key = get_random_string(session_key_length)
        user.save()
