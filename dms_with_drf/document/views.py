from rest_framework import viewsets
from rest_framework.parsers import MultiPartParser, FormParser
from .permissions import DocumentPermission
from .serializers import DocumentSerializer
from .models import Document

class DocumentViewSet(viewsets.ModelViewSet):
    queryset = Document.objects.all().order_by("-uploaded_at")
    serializer_class = DocumentSerializer
    parser_classes = [MultiPartParser, FormParser]
    permission_classes = [DocumentPermission]

    def perform_create(self, serializer):
        serializer.save(uploaded_by=self.request.user)
