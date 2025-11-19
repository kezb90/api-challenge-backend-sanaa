from rest_framework import serializers
from .models import Document

class DocumentSerializer(serializers.ModelSerializer):
    uploaded_by = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Document
        fields = ["id", "title", "file", "uploaded_by", "uploaded_at", "updated_at"]
        read_only_fields = ["uploaded_by", "uploaded_at", "updated_at"]
