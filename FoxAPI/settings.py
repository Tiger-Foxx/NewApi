import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-g*3q_vkqd-4wv8c^!ln22os*bdiv^+z(l7wjg*_$9f*r0lyblp'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*', 'theoldfox.pythonanywhere.com', '127.0.0.1','apifox.pythonanywhere.com']

# Application definition

INSTALLED_APPS = [
    'api',
    'rest_framework',
    'rest_framework.authtoken',  # Ajout de l'app d'authentification par token
    'corsheaders',
    'django_filters', # Ajouter cette ligne

    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',  # Important pour React
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'FoxAPI.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'FoxAPI.wsgi.application'

# Database - Nous utiliserons la base de données existante
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',  # Assure-toi que ton ancien fichier db.sqlite3 est ici
    }
}

# Password validation
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
LANGUAGE_CODE = 'fr-fr'
TIME_ZONE = 'Africa/Douala'
USE_I18N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

# Media files
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')  # Assure-toi que ton dossier media est ici

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# DRF settings
# Configuration de DRF
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'api.authentication.ExpiringTokenAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ],
    'DEFAULT_FILTER_BACKENDS': ['django_filters.rest_framework.DjangoFilterBackend'], # DjangoFilterBackend est ici pour les filtres par champ

    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.AllowAny',
    ],
    # MODIFICATION ICI:
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
    # 'PAGE_SIZE': 22 # PAGE_SIZE est toujours utile comme taille par défaut si limit n'est pas fourni
                     # ou peut être enlevé si vous voulez toujours spécifier limit.
                     # Avec LimitOffsetPagination, PAGE_SIZE devient default_limit.
    # Vous pouvez aussi définir des limites max si vous le souhaitez :
    # 'DEFAULT_LIMIT': 22, # Nommé 'PAGE_SIZE' dans la doc mais agit comme default_limit
    # 'MAX_LIMIT': 100, # Pour éviter que les clients demandent trop de données
}


# CORS settings pour permettre au frontend React d'accéder à l'API
CORS_ALLOW_ALL_ORIGINS = True  # En développement seulement, à restreindre en production

# Configuration email
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'tigerfox750@gmail.com'
EMAIL_HOST_PASSWORD = 'rltrfyxinepnqazp'
TOKEN_EXPIRED_AFTER_SECONDS = 14 * 24 * 60 * 60

ADMIN_EMAIL_NOTIFICATIONS = 'donfackarthur750@gmail.com'
DEFAULT_FROM_EMAIL = 'Fox <'+EMAIL_HOST_USER+'>'