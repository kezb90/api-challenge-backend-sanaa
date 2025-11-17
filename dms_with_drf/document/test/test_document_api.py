import io
from django.urls import reverse
from django.contrib.auth.models import Group
from accounts.models import User
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from unittest.mock import patch

from document.models import Document

class DocumentAPITestCase(APITestCase):

    def setUp(self):
        # Create groups
        for role in ["admin", "editor", "viewer"]:
            Group.objects.get_or_create(name=role)

        # Users
        self.admin  = User.objects.create_user(username="admin",  email="admin@test.com",  password="123")
        self.editor = User.objects.create_user(username="editor", email="editor@test.com", password="123")
        self.viewer = User.objects.create_user(username="viewer", email="viewer@test.com", password="123")

        self.admin.groups.add(Group.objects.get(name="admin"))
        self.editor.groups.add(Group.objects.get(name="editor"))
        self.viewer.groups.add(Group.objects.get(name="viewer"))

        self.client = APIClient()
        self.url_list = "/document/documents/"
        
        from django.core.files.uploadedfile import SimpleUploadedFile

        self.file_data = SimpleUploadedFile(
            name="test.pdf",
            content=b"This is a fake PDF file for testing purposes.",
            content_type="application/pdf"
        )

    def authenticate(self, user):
        self.client.force_authenticate(user=user)

    # -----------------------------
    # Viewer Tests
    # -----------------------------
    def test_viewer_can_list_documents(self):
        self.authenticate(self.viewer)
        response = self.client.get(self.url_list)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_viewer_cannot_upload_document(self):
        self.authenticate(self.viewer)
        response = self.client.post(self.url_list, {"title": "x", "file": self.file_data})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_viewer_cannot_update_document(self):
        doc = Document.objects.create(title="t1", uploaded_by=self.editor, file=self.file_data)
        self.authenticate(self.viewer)
        response = self.client.patch(f"{self.url_list}{doc.id}/", {"title": "new"})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_viewer_cannot_delete_document(self):
        doc = Document.objects.create(title="t1", uploaded_by=self.editor, file=self.file_data)
        self.authenticate(self.viewer)
        response = self.client.delete(f"{self.url_list}{doc.id}/")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    # -----------------------------
    # Editor Tests
    # -----------------------------
    @patch("storages.backends.s3boto3.S3Boto3Storage.save")
    def test_editor_can_upload_document(self, mock_storage):
        mock_storage.return_value = "mocked-path/test.jpg"
        self.authenticate(self.editor)

        response = self.client.post(self.url_list, {"title": "doc1", "file": self.file_data})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    @patch("storages.backends.s3boto3.S3Boto3Storage.save")
    def test_editor_can_update_document(self, mock_storage):
        mock_storage.return_value = "mocked-path/test.jpg"

        doc = Document.objects.create(title="orig", uploaded_by=self.editor, file=self.file_data)

        self.authenticate(self.editor)
        response = self.client.patch(f"{self.url_list}{doc.id}/", {"title": "new title"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], "new title")

    def test_editor_cannot_delete_document(self):
        doc = Document.objects.create(title="orig", uploaded_by=self.editor, file=self.file_data)
        
        self.authenticate(self.editor)
        response = self.client.delete(f"{self.url_list}{doc.id}/")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    # -----------------------------
    # Admin Tests
    # -----------------------------
    @patch("storages.backends.s3boto3.S3Boto3Storage.save")
    def test_admin_can_upload_document(self, mock_storage):
        mock_storage.return_value = "mocked-path/test.jpg"

        self.authenticate(self.admin)
        response = self.client.post(self.url_list, {"title": "doc", "file": self.file_data})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_admin_can_update_document(self):
        doc = Document.objects.create(title="d1", uploaded_by=self.admin, file=self.file_data)

        self.authenticate(self.admin)
        response = self.client.patch(f"{self.url_list}{doc.id}/", {"title": "updated"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_admin_can_delete_document(self):
        doc = Document.objects.create(title="d2", uploaded_by=self.admin, file=self.file_data)

        self.authenticate(self.admin)
        response = self.client.delete(f"{self.url_list}{doc.id}/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
