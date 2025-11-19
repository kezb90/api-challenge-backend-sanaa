from rest_framework import viewsets, status
from rest_framework.response import Response
from rbac.permissions import IsAdmin
from django.contrib.auth import get_user_model

from .serializers import UserCreateSerializer, UserSerializer

User = get_user_model()

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    permission_classes = [IsAdmin]

    def get_serializer_class(self):
        if self.action == "create":
            return UserCreateSerializer
        return UserSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        return Response({
            "detail": "کاربر با موفقیت ایجاد شد",
            "user": UserSerializer(user).data
        }, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        return Response({"detail": "تغییر کاربر از این endpoint مجاز نیست"}, status=403)

    def partial_update(self, request, *args, **kwargs):
        return Response({"detail": "تغییر کاربر از این endpoint مجاز نیست"}, status=403)
