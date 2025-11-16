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
        
        # خروجی درست: اطلاعات کاربر + پیام
        return Response({
            "detail": "کاربر با موفقیت ایجاد شد",
            "user": UserSerializer(user).data
        }, status=status.HTTP_201_CREATED)
