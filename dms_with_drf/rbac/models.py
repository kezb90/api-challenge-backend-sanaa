from django.contrib.auth.models import AbstractUser, Group
from django.db import models

class Role(models.Model):
    ADMIN = 'admin'
    EDITOR = 'editor'
    VIEWER = 'viewer'
    
    ROLE_CHOICES = [
        (ADMIN, 'Admin'),
        (EDITOR, 'Editor'),
        (VIEWER, 'Viewer'),
    ]
    
    name = models.CharField(max_length=20, choices=ROLE_CHOICES, unique=True)
    
    def __str__(self):
        return self.name

class RolePermission(models.Model):
    role = models.ForeignKey(Role, on_delete=models.CASCADE)
    codename = models.CharField(max_length=100)  #"can_upload_document"
    
    class Meta:
        unique_together = ('role', 'codename')