"""Configuration du service Dresseurs : tout vient des variables d'environnement."""
import os

SECRET_KEY = os.getenv("DJANGO_SECRET_KEY", "dev-only-change-me")
DEBUG = os.getenv("DEBUG", "0") == "1"
ALLOWED_HOSTS = ["*"]  # service joignable uniquement sur le réseau Docker interne

JWT_SECRET = os.getenv("JWT_SECRET", "dev-secret-change-me")
JWT_EXPIRES_MINUTES = 360  # même durée que l'ancien monolithe

INSTALLED_APPS = [
    "rest_framework",
    "accounts",
]

MIDDLEWARE = ["django.middleware.common.CommonMiddleware"]

ROOT_URLCONF = "config.urls"
WSGI_APPLICATION = "config.wsgi.application"
APPEND_SLASH = False  # le front appelle /users et non /users/

if os.getenv("POSTGRES_HOST"):
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "HOST": os.environ["POSTGRES_HOST"],
            "PORT": os.getenv("POSTGRES_PORT", "5432"),
            "NAME": os.getenv("POSTGRES_DB", "dresseurs"),
            "USER": os.getenv("POSTGRES_USER", "poke"),
            "PASSWORD": os.getenv("POSTGRES_PASSWORD", "poke"),
        }
    }
else:  # développement hors Docker
    DATABASES = {"default": {"ENGINE": "django.db.backends.sqlite3", "NAME": "db.sqlite3"}}

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
USE_TZ = True

# L'authentification est faite par la gateway : DRF n'a rien à vérifier lui-même
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [],
    "DEFAULT_PERMISSION_CLASSES": [],
    "UNAUTHENTICATED_USER": None,
    "DEFAULT_RENDERER_CLASSES": ["rest_framework.renderers.JSONRenderer"],
}
