from django.urls import path

from remauth.api.views import login_token_view, details_view
from .views import remote_login_view

app_name = "remauth"

urlpatterns = [
    path("details/", view=details_view),
    path("verify/<str:email>/<str:token>/", view=remote_login_view),
    path("api/generate/", view=login_token_view),
]
