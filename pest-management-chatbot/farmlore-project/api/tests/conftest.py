"""Test configuration for the pest management chatbot."""
import pytest
from django.conf import settings

def pytest_configure():
    """Configure Django settings for tests."""
    settings.configure(
        SECRET_KEY='test-secret-key',
        DEBUG=False,
        DATABASES={
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': ':memory:'
            }
        },
        INSTALLED_APPS=[
            'django.contrib.contenttypes',
            'django.contrib.auth',
            'rest_framework',
            'api',
        ],
        ROOT_URLCONF='core.urls',
        REST_FRAMEWORK={
            'TEST_REQUEST_DEFAULT_FORMAT': 'json'
        },
        MIDDLEWARE=[
            'django.middleware.security.SecurityMiddleware',
            'django.contrib.sessions.middleware.SessionMiddleware',
            'django.middleware.common.CommonMiddleware',
            'django.middleware.csrf.CsrfViewMiddleware',
            'django.contrib.auth.middleware.AuthenticationMiddleware',
            'django.contrib.messages.middleware.MessageMiddleware',
            'django.middleware.clickjacking.XFrameOptionsMiddleware',
        ],
    )
