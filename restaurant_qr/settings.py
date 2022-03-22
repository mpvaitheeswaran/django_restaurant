

from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-z3cq%@d2idrcuakg!qcf3n1qqg%%^flvlb)!i--&11ed@iawbf'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

AUTH_USER_MODEL = 'accounts.CustomUser'

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'qrmenu.apps.QrmenuConfig',
    'accounts.apps.AccountsConfig',
    'qradmin.apps.QradminConfig',
    'crispy_forms',
    'notifications',
    'currencies',
    'payments',
]
CRISPY_TEMPLATE_PACK = 'bootstrap4'

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'restaurant_qr.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'qrmenu.context_processors.add_variable_to_context',
                'django.template.context_processors.static',
                'currencies.context_processors.currencies',
            ],
        },
    },
]


WSGI_APPLICATION = 'restaurant_qr.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'restaurant_qr_dj2.1.15',
        'USER': 'postgres',
        'PASSWORD': 'postgres',
        'HOST': 'localhost',
    }
}

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql',
#         'NAME': 'restaurant_qr_test',
#         'USER': 'postgres',
#         'PASSWORD': 'postgres',
#         'HOST': 'localhost',
#     }
# }

# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/3.2/topics/i18n/

# import currencies
# python manage.py currencies --import=USD

OPENEXCHANGERATES_APP_ID = "c2b2efcb306e075d9c2f2d0b614119ea"

DEFAULT_CURRENCY = 'INR'

LANGUAGE_CODE = 'en-us'

#TIME_ZONE = 'UTC'
TIME_ZONE =  'Asia/Kolkata'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS = [
    BASE_DIR/'static'
]
STATIC_ROOT = (BASE_DIR/'asset')

MEDIA_URL = '/media/'
MEDIA_ROOT = (BASE_DIR/'media')

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

#Redirect Urls
LOGIN_REDIRECT_URL = 'dashboard'
LOGIN_URL = 'accounts-login'
LOGOUT_REDIRECT_URL = 'accounts-logout'

# Email Test
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

#Email Config
# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# EMAIL_HOST = 'smtp.gmail.com'
# EMAIL_PORT = 587
# EMAIL_USE_TLS = True
# EMAIL_HOST_USER = 'username@gmail.com'
# EMAIL_HOST_PASSWORD = 'your_password'

# PayTm Payment Gateway
PAYTM_COMPANY_NAME = "BUYP Technologies"   # For representation purposes 
# PAYTM_MERCHANT_KEY = "VaVxV@xUiPTJ6%Kx"
# PAYTM_MERCHANT_ID = "lSLEKI68544857587304"
PAYTM_MERCHANT_KEY = "bI5q_AgRQVCkQVm5"
PAYTM_MERCHANT_ID = "CJhAzb77364189315875"
PAYTM_CALLBACK_URL = "http://localhost:8000/payments/response/" # Hardcode
# PAYTM_WEBSITE = "WEBSTAGING"
PAYTM_WEBSITE = "DEFAULT"
# PAYTM_PAYMENT_GATEWAY_URL = "https://securegw-stage.paytm.in/order/process"
# PAYTM_TRANSACTION_STATUS_URL = "https://securegw-stage.paytm.in/order/status"
PAYTM_PAYMENT_GATEWAY_URL = "https://securegw.paytm.in/theia/processTransaction"
PAYTM_TRANSACTION_STATUS_URL = "https://securegw.paytm.in/order/status"
