from rest_framework import serializers


class RemoteUserSerializer(serializers.Serializer):
    email = serializers.EmailField()
