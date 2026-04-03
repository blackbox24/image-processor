from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()


class SignUpSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True)

    def validate_username(self, username):
        user_exists = User.objects.filter(username=username)
        if user_exists:
            raise serializers.ValidationError("Username already exists")
        return username
