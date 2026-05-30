from django.contrib.auth import get_user_model
from rest_framework import serializers


User = get_user_model()


class UserSerializer(serializers.ModelSerializer[User]):
    class Meta:
        model = User
        fields = (
            "id",
            "email",
            "first_name",
            "last_name",
            "password",
            "is_staff"
        )
        read_only_fields = ("id", "is_staff")
        extra_kwargs = {
            "password": {
                "write_only": True,
                "min_length": 8,
                "style": {"input_type": "password"},
                "trim_whitespace": False
            }
        }
