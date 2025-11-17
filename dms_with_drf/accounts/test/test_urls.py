# accounts/tests/test_urls.py
from django.test import TestCase
from django.urls import reverse, resolve
from accounts.views import UserViewSet
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


class UrlsTest(TestCase):
    """تست‌های URLهای accounts"""
    
    def test_user_list_url(self):
        """تست URL لیست کاربران"""
        url = reverse('user-list')  # تغییر از userview-list به user-list
        self.assertEqual(resolve(url).func.cls, UserViewSet)

    def test_user_detail_url(self):
        """تست URL جزئیات کاربر"""
        url = reverse('user-detail', args=[1])  # تغییر از userview-detail به user-detail
        self.assertEqual(resolve(url).func.cls, UserViewSet)

    def test_token_obtain_url(self):
        """تست URL دریافت توکن JWT"""
        url = reverse('token_obtain_pair')
        self.assertEqual(resolve(url).func.view_class, TokenObtainPairView)

    def test_token_refresh_url(self):
        """تست URL رفرش توکن JWT"""
        url = reverse('token_refresh')
        self.assertEqual(resolve(url).func.view_class, TokenRefreshView)

    def test_url_patterns_exist(self):
        """تست وجود تمام URLهای مورد نیاز"""
        # لیست کاربران
        url = reverse('user-list')
        self.assertEqual(url, '/api/users/')
        
        # جزئیات کاربر
        url = reverse('user-detail', args=[1])
        self.assertEqual(url, '/api/users/1/')
        
        # دریافت توکن
        url = reverse('token_obtain_pair')
        self.assertEqual(url, '/api/token/')
        
        # رفرش توکن
        url = reverse('token_refresh')
        self.assertEqual(url, '/api/token/refresh/')