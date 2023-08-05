import logging
from django.conf import settings
from django.core.cache import cache
from django.contrib.auth import get_user_model, login
from django.shortcuts import redirect
from django.views.generic import View
from django.contrib import messages

log = logging.getLogger(__name__)

User = get_user_model()

try:
    auth_backend = settings.REMAUTH_DEFAULT_AUTH_BACKEND
except AttributeError:
    auth_backend = "django.contrib.auth.backends.ModelBackend"


class RemoteLoginView(View):
    def get(self, *args, **kwargs):
        email = kwargs["email"]
        token = kwargs["token"]

        log.info(f"Remote login attempt. User: {email}")

        saved_token = cache.get(f"remauth_token:{email}")

        if saved_token == token:
            user = User.objects.get(email=email)
            login(
                self.request, user, backend=auth_backend
            )
            self.request.session.set_expiry(0)
            messages.success(self.request, "Successfully logged in.")

            return redirect(settings.REMAUTH_SUCCESS_URL)

        log.error(f"Failed to login user {email}.")
        messages.error(self.request, "Invalid token")
        return redirect("/")


remote_login_view = RemoteLoginView.as_view()
