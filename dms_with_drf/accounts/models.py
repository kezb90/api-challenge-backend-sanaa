# accounts/models.py
from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    email = models.EmailField(unique=True, blank=False, null=False)

    def has_role(self, role_name):
        return self.groups.filter(name=role_name).exists()
    
    @property
    def role(self):
        if self.is_superuser:
            return 'admin'
        group = self.groups.first()
        return group.name if group else 'viewer'

    def __str__(self):
        return self.get_full_name() or self.username