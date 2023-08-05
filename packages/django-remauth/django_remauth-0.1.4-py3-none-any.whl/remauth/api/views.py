import secrets
import logging
from django.conf import settings
from django.core.cache import cache
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .serializers import RemoteUserSerializer

log = logging.getLogger(__name__)

CACHE_EXPIRY = 60 * 5  # 300 Seconds = 5 Minutes


class LoginTokenView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, IsAdminUser]

    def post(self, request):
        serializer = RemoteUserSerializer(data=request.data)
        log.info(f"Attempt to generate login token. User: {serializer.initial_data['email']}")
        if serializer.is_valid():
            token = secrets.token_urlsafe(40)
            cache.set(
                f"remauth_token:{serializer.validated_data['email']}",
                token,
                CACHE_EXPIRY,
            )

            return Response({"token": token}, status=status.HTTP_202_ACCEPTED)

        log.error(f'Failed to generate login token. Invalid serializer. User: {serializer.initial_data["email"]}')
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


login_token_view = LoginTokenView.as_view()


class DetailsView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, IsAdminUser]

    def get(self, request):
        log.info("Fetching details remotely.")
        try:
            data = settings.REMAUTH_GET_DATA
        except AttributeError:
            data = {
            }
        return Response(data, status=status.HTTP_200_OK)


details_view = DetailsView.as_view()
