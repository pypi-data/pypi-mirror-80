# django-admin-safe-login

Add captcha field and rsa encryption password field for django admin's login page.

## Install

```shell
pip install django-admin-safe-login
```

## Usage

**pro/settings.py**

```python
INSTALLED_APPS = [
    ...
    'django_static_jquery3',
    'django_secure_password_input',
    'django_simple_tags',
    'captcha',
    'django_admin_safe_login',
    ...
]

CAPTCHA_IMAGE_SIZE = (100, 30)  # required
DJANGO_ADMIN_SAFE_LOGIN_ENABLE_CAPTCHA = True # optional, default to True
DJANGO_ADMIN_SAFE_LOGIN_BACKGROUND_IMAGE = "django-admin-safe-login/img/example-background.jpg"  # optional, default to no-image.
DJANGO_ADMIN_SAFE_LOGIN_BOX_MARGIN_RIGHT = "200px" # optional, default to auto
DJANGO_ADMIN_SAFE_LOGIN_BOX_MARGIN_LEFT = "auto" # optional, default to auto
DJANGO_ADMIN_SAFE_LOGIN_BOX_MARGIN_TOP = "100px" # optional, default to 100px
DJANGO_ADMIN_SAFE_LOGIN_BOX_MARGIN_BOTTOM = "100px" # optional, default to 100px
DJANGO_ADMIN_SAFE_LOGIN_TEMPLATE = "" # optional, default to "admin/login.html".
```

**Note:**

1. Insert django_static_jquery3, django_secure_password_input, django-simple-tags, captcha and django_admin_safe_login into INSTALLED_APPS.
1. Application django_static_jquery3 provides static jquery.js.
1. Application django_secure_password_input provides rsa encryption and decryption function for password field.
1. Application django_admin_safe_login provides all functions about safe login.
1. Application captcha provides image captcha functions.
1. Application django-simple-tags provides custom template tags used in our admin/login.html.
1. Configuration item CAPTCHA_IMAGE_SIZE is required, and must set to (100, 30) so that it will not break the display style. If you want other size image, you have to rewrite some css code.
1. Configurations about password RSA encryption, see details at https://pypi.org/project/django-secure-password-input/.
1. Configurations about captcha, see detail at https://pypi.org/project/django-simple-captcha/.
1. Configurations about password reset, see detail at https://docs.djangoproject.com/en/3.0/ref/contrib/admin/ (search: Adding a password reset feature).

**pro/urls.py**

```python
from django.urls import path
from django.urls import include

urlpatterns = [
    ...
    path('captcha/', include("captcha.urls")),
    ...
]
```

**Note:**

1. Include captcha.urls is required so that the captcha image can be displayed.

## Changes about admin/login.html

We have override some part of admin/login.html. But the admin/login.html content may change in future releases. So you should known what part is overrided.

1. Our new admin/login.html extends from system's admin/login.html.
1. We override the extrastyle block to add extra js and css.
1. The function adding background image and changing login box position is implemented in our new extrastyle block.
1. We override the whole content block.
1. We copied the whole content block from django's default admin/login.html.
1. We added blocks inside content block: form, form-row-username, from-row-password, form-row-extra, form-row-captcha, password-reset-url, before-submit-row, submit-row, after-submit-row.



## Releases

### v0.3.3 2020/09/24

- Add app_requires.
- Add License file.

### v0.3.2 2020/09/01

- Depends on django-secure-password-input>=0.1.1.

### v0.3.1 2020/09/01

- Rename zh_Hans to zh_hans.
- Depends on django-static-jquery3>=5.0.0.

### v0.3.0 2020/05/20

- Add background image setting.
- Add login box position setting.
- Use admin/login.html override instead of creating a new template.
- Fix document.
- Fix translation.
- Fix setup.py problem that include demo and example code in the final package.

### v0.2.0 2020/03/07

- Add rsa encryption and decrption functions for password field.
- Fix requirements.txt missing django-static-jquery3 problem.

### v0.1.0 2020/03/06

- First release.