import os
from pathlib import Path
import environ

# Initialize environ
env = environ.Env(
    DEBUG=(bool, False),
    DB_NAME=(str, 'farmlore'),
    DB_USER=(str, 'postgres'),
    DB_PASSWORD=(str, 'postgres'),  # Changed to match docker-compose.yml
    DB_HOST=(str, 'db'),  # Changed from 'localhost' to 'db' for Docker Compose
    DB_PORT=(str, '5432'),
    DISABLE_PROLOG=(bool, False),
    USE_OLLAMA=(bool, True),
    OLLAMA_BASE_URL=(str, 'http://ollama:11434'),
    OLLAMA_MODEL=(str, 'farmlore-general')
)

# Build paths inside the project
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-key-for-development'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env('DEBUG')

ALLOWED_HOSTS = ['localhost', '127.0.0.1', 'web']

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # Third-party apps
    'rest_framework',
    
    # Project apps
    'core',
    'ml',
    'api',
    'chatbot',
    'community.apps.CommunityConfig',
    'community.templatetags',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'farmlore.urls'

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

WSGI_APPLICATION = 'farmlore.wsgi.application'

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': env('DB_NAME'),
        'USER': env('DB_USER'),
        'PASSWORD': env('DB_PASSWORD'),
        'HOST': env('DB_HOST'),
        'PORT': env('DB_PORT'),
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
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = 'static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]

# Media files
MEDIA_URL = 'media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# REST Framework
REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticatedOrReadOnly',
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10
}

# OpenAI API Key
OPENAI_API_KEY = ''

# Data and model paths
DATA_DIR = os.path.join(BASE_DIR, 'data')
RAW_DATA_DIR = os.path.join(DATA_DIR, 'raw')
PROCESSED_DATA_DIR = os.path.join(DATA_DIR, 'processed')
MODEL_DIR = os.path.join(DATA_DIR, 'models')

# Create directories if they don't exist
for directory in [DATA_DIR, RAW_DATA_DIR, PROCESSED_DATA_DIR, MODEL_DIR]:
    os.makedirs(directory, exist_ok=True)

# Dataset URLs
DATASET_URLS = {
    'pests': 'https://hebbkx1anhila5yf.public.blob.vercel-storage.com/pests_final_3-81HePx2jC2tph3HpkjnHEzDmST45ZW.csv',
    'methods': 'https://hebbkx1anhila5yf.public.blob.vercel-storage.com/methods_final_3-WCyLl9LDln0Lvsh5wS1JLwopqvnG8v.csv',
    'soil': 'https://hebbkx1anhila5yf.public.blob.vercel-storage.com/indigenous_soil_fertilization%20%281%29-KhueF0T67nRNVCqGrYChQSyoaVPA7Y.csv',
}

# Authentication settings
LOGIN_REDIRECT_URL = '/community/'
LOGOUT_REDIRECT_URL = '/'

# API version and environment
API_VERSION = '1.0.0'
ENVIRONMENT = os.environ.get('ENVIRONMENT', 'development')

# Ollama settings
USE_OLLAMA = env('USE_OLLAMA')
OLLAMA_BASE_URL = env('OLLAMA_BASE_URL')
OLLAMA_MODEL = env('OLLAMA_MODEL')