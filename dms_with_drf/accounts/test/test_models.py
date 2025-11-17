# accounts/tests/test_models.py
from django.test import TestCase
from django.contrib.auth.models import Group
from accounts.models import User


class UserModelTest(TestCase):
    """تست‌های مدل User"""
    
    def setUp(self):
        # ایجاد گروه‌های RBAC مورد نیاز
        self.admin_group, _ = Group.objects.get_or_create(name='admin')
        self.editor_group, _ = Group.objects.get_or_create(name='editor')
        self.viewer_group, _ = Group.objects.get_or_create(name='viewer')
        
        self.user_data = {
            'username': 'testuser',
            'password': 'TestPass123!',
            'email': 'test@example.com',
            'first_name': 'Test',
            'last_name': 'User'
        }

    def test_create_user_with_valid_data(self):
        """تست ایجاد کاربر با داده‌های معتبر"""
        user = User.objects.create_user(**self.user_data)
        
        self.assertEqual(user.username, 'testuser')
        self.assertEqual(user.email, 'test@example.com')
        self.assertTrue(user.check_password('TestPass123!'))
        self.assertFalse(user.is_superuser)
        self.assertFalse(user.is_staff)
        self.assertTrue(user.is_active)

    def test_create_superuser(self):
        """تست ایجاد سوپر کاربر"""
        superuser = User.objects.create_superuser(
            username='superadmin',
            email='admin@example.com',
            password='AdminPass123!'
        )
        
        self.assertTrue(superuser.is_superuser)
        self.assertTrue(superuser.is_staff)
        self.assertEqual(superuser.role, 'admin')

    def test_email_unique_constraint(self):
        """تست یکتا بودن ایمیل"""
        User.objects.create_user(**self.user_data)
        
        # باید خطای یکتایی بدهد
        with self.assertRaises(Exception):
            User.objects.create_user(
                username='testuser2',
                email='test@example.com',  # همان ایمیل
                password='testpass123'
            )

    def test_has_role_method(self):
        """تست متد has_role برای بررسی نقش کاربر"""
        user = User.objects.create_user(**self.user_data)
        user.groups.add(self.viewer_group)
        
        self.assertTrue(user.has_role('viewer'))
        self.assertFalse(user.has_role('admin'))
        self.assertFalse(user.has_role('editor'))

    def test_role_property_for_different_users(self):
        """تست property role برای کاربران با نقش‌های مختلف"""
        # کاربر viewer
        viewer_user = User.objects.create_user(**self.user_data)
        viewer_user.groups.add(self.viewer_group)
        self.assertEqual(viewer_user.role, 'viewer')

        # کاربر editor
        editor_user = User.objects.create_user(
            username='editor',
            email='editor@example.com',
            password='testpass123'
        )
        editor_user.groups.add(self.editor_group)
        self.assertEqual(editor_user.role, 'editor')

        # کاربر admin
        admin_user = User.objects.create_user(
            username='adminuser',
            email='adminuser@example.com',
            password='testpass123'
        )
        admin_user.groups.add(self.admin_group)
        self.assertEqual(admin_user.role, 'admin')

        # سوپر کاربر
        superuser = User.objects.create_superuser(
            username='super',
            email='super@example.com',
            password='testpass123'
        )
        self.assertEqual(superuser.role, 'admin')

        # کاربر بدون گروه
        no_group_user = User.objects.create_user(
            username='nogroup',
            email='nogroup@example.com',
            password='testpass123'
        )
        self.assertEqual(no_group_user.role, 'viewer')

    def test_string_representation(self):
        """تست نمایش رشته‌ای مدل User"""
        user = User.objects.create_user(**self.user_data)
        expected_name = f"{user.first_name} {user.last_name}"
        self.assertEqual(str(user), expected_name)

        # تست زمانی که نام و نام خانوادگی خالی است
        user2 = User.objects.create_user(
            username='user2',
            email='user2@example.com',
            password='testpass123'
        )
        self.assertEqual(str(user2), 'user2')