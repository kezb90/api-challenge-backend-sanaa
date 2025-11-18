# Sanaap DMS API  
پروژه مدیریت اسناد (Document Management System) با استفاده از Django REST Framework، PostgreSQL، Redis و MinIO  
و با پشتیبانی از JWT Authentication و Swagger UI.

---

## 🚀 راه‌اندازی پروژه



برای اجرای پروژه با Docker، مراحل زیر را انجام دهید:

### 1. ساخت DevContainer

اگر از VSCode و DevContainer استفاده می‌کنید، کافی است DevContainer را باز کنید:

- فایل `.devcontainer/docker-compose.yml` و `.devcontainer/Dockerfile` تمام وابستگی‌ها را مدیریت می‌کنند.
- `mc` (MinIO Client) به صورت خودکار نصب می‌شود.
- با اجرای `postStartCommand`:
  - دیتابیس مهاجرت می‌شود (`migrate`)
  - باکت MinIO ساخته می‌شود.

### 2. اجرای Docker Compose دستی (در صورت نیاز)

```bash
docker-compose up -d --build

docker-compose exec app bash


ابتدا وارد پوشه پروژه شوید:

```bash
cd dms_with_drf
```

سپس برای ساخت اکانت مدیریت دستور زیر را اجرا کنید:

```bash
python manage.py createsuperuser
```

بعد از اجرای این دستور، اطلاعات زیر را وارد کنید:

- **Username**
- **Email**
- **Password**

سپس پروژه را اجرا کنید:

```bash
python manage.py runserver
```

اکنون APIها و Swagger در آدرس زیر در دسترس‌اند:

```
http://127.0.0.1:8000/
```

---

## 🔐 دریافت توکن JWT

برای استفاده از APIها ابتدا باید **Access Token** دریافت کنید.

به مسیر زیر مراجعه کنید:

```
/accounts/api/token/
```

و با ارسال `username` و `password` یک توکن دریافت کنید.

نمونه درخواست:

```json
POST /accounts/api/token/
{
  "username": "admin",
  "password": "your_password"
}
```

خروجی:

```json
{
  "refresh": "xxxx",
  "access": "yyyy"
}
```

---

## 🧩 فعال‌سازی دسترسی در Swagger

برای استفاده از APIها از طریق SwaggerUI:

1. روی دکمه **Authorize** کلیک کنید  
2. در قسمت `value` مقدار زیر را وارد کنید:

```
Bearer <access_token>
```

مثال:

```
Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

3. اکنون تمام APIها برای شما فعال خواهند شد.

---

## 👥 نقش‌ها (RBAC Roles)

نقش‌هایی که می‌توانید در سیستم تعریف کنید تنها شامل موارد زیر است:

- **admin**
- **editor**
- **viewer**

هر نقش دارای سطح دسترسی مشخصی برای مشاهده، ویرایش یا مدیریت اسناد است.

---

## 📂 ساختار APIها

### Accounts  
```
/accounts/api/users/                → مدیریت کاربران  
/accounts/api/token/                → دریافت توکن JWT  
/accounts/api/token/refresh/        → رفرش توکن  
```

### Documents  
```
/document/documents/                → CRUD اسناد  
```

فایل‌ها از طریق `multipart/form-data` آپلود شده  
و در MinIO ذخیره می‌شوند.

---

## 🗄 تکنولوژی‌های مورد استفاده

- **Django 5 + DRF**
- **PostgreSQL**
- **Redis 7**
- **MinIO (S3 Compatible Storage)**
- **DRF-YASG (Swagger UI)**
- **JWT Authentication**
- **RBAC Permission System**

---

## 💡 نکته مهم
برای آپلود یا مشاهده اسناد، کاربر باید **احراز هویت شده** باشد  
و نقش او باید اجازه انجام عملیات را داشته باشد.

---

## 📞 پشتیبانی
در صورت نیاز به توسعه بیشتر، ماژول جدید یا رفع مشکل، با من در تماس باشید.
