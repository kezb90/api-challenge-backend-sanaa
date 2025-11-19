from django.db.models.signals import post_migrate
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.dispatch import receiver
from document.models import Document

@receiver(post_migrate)
def create_roles(sender, **kwargs):
    if sender.label != "document":
        return

    content_type = ContentType.objects.get_for_model(Document)
    perms = Permission.objects.filter(content_type=content_type)

    viewer_perms = perms.filter(codename="view_document")
    editor_perms = perms.filter(codename__in=["view_document", "add_document", "change_document"])
    admin_perms = perms

    viewer_group, _ = Group.objects.get_or_create(name="viewer")
    editor_group, _ = Group.objects.get_or_create(name="editor")
    admin_group, _ = Group.objects.get_or_create(name="admin")

    viewer_group.permissions.set(viewer_perms)
    editor_group.permissions.set(editor_perms)
    admin_group.permissions.set(admin_perms)
