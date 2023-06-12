from rest_framework import serializers
from users.models import User


class UserSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)

    email = serializers.EmailField(max_length=127)
    username = serializers.CharField(max_length=150)
    password = serializers.CharField(write_only=True)
    is_employee = serializers.BooleanField(required=False, default=False)

    is_superuser = serializers.BooleanField(read_only=True)

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("email already registered.")
        return value

    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("username already taken.")
        return value

    def create(self, validated_data):
        password = validated_data.pop("password")
        is_employee = validated_data.pop("is_employee", False)
        is_superuser = False

        if is_employee:
            is_superuser = True

        user = User(**validated_data)
        user.set_password(password)
        user.is_employee = is_employee
        user.is_superuser = is_superuser
        user.save()
        return user
