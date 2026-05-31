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

    def create(self, validated_data: dict) -> User:
        return User.objects.create_user(**validated_data)

    def update(self, instance: User, validated_data: dict) -> User:
        password = validated_data.pop("password", None)
        user = super().update(instance, validated_data)

        if password:
            user.set_password(password)
            user.save()

        return user


class UserAdminSerializer(UserSerializer):
    class Meta(UserSerializer.Meta):
        fields = UserSerializer.Meta.fields + (
            "is_superuser",
            "last_login",
            "date_joined",
            "user_permissions",
            "groups"
        )
        read_only_fields = UserSerializer.Meta.read_only_fields + (
            "last_login",
            "date_joined"
        )


class UserAdminListRetrieveSerializer(UserAdminSerializer):
    user_permissions = serializers.StringRelatedField(many=True)
    groups = serializers.StringRelatedField(many=True)
