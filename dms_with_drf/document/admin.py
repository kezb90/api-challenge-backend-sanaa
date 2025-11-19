# document/admin.py
from django.contrib import admin
from .models import Document

@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "uploaded_by", "uploaded_at", "updated_at")
    list_filter = ("uploaded_by", "uploaded_at")
    search_fields = ("title", "uploaded_by__username")
    readonly_fields = ("uploaded_at", "updated_at")
