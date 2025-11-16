from django.apps import AppConfig
from django.db.models.signals import post_migrate

def create_roles(sender, **kwargs):
    from django.contrib.auth.models import Group
    for role in ['admin', 'editor', 'viewer']:
        Group.objects.get_or_create(name=role)

class RbacConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'rbac'

    def ready(self):
        post_migrate.connect(create_roles, sender=self)