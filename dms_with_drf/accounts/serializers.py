from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group

User = get_user_model()

VALID_ROLES = ["viewer", "editor", "admin"]

class UserCreateSerializer(serializers.ModelSerializer):
    role = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ("id", "username", "password", "first_name", "last_name", "email", "role")
        extra_kwargs = {"password": {"write_only": True}}

    def validate_role(self, role):
        if role not in VALID_ROLES:
            raise serializers.ValidationError("نقش نامعتبر است")
        return role

    def create(self, validated_data):
        role_name = validated_data.pop("role")
        password = validated_data.pop("password")
        request_user = self.context["request"].user

        # فقط admin یا superuser می‌توانند نقش بدهند
        if not (
            request_user.is_superuser 
            or request_user.groups.filter(name="admin").exists()
        ):
            raise serializers.ValidationError("فقط admin می‌تواند نقش تعیین کند")

        # فقط superuser می‌تواند کاربر admin بسازد
        if role_name == "admin" and not request_user.is_superuser:
            raise serializers.ValidationError("فقط superuser می‌تواند admin بسازد")

        user = User.objects.create_user(password=password, **validated_data)

        group = Group.objects.get(name=role_name)
        user.groups.add(group)

        return user

class UserSerializer(serializers.ModelSerializer):
    role = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ("id", "username", "first_name", "last_name", "email", "role")

    def get_role(self, obj):
        return obj.role