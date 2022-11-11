from .base import *
import dj_database_url

DEBUG = False


# db_from_env = dj_database_url.config(conn_max_age=500)
# DATABASES['default'].update(db_from_env)

DATABASES = {
    "default": dj_database_url.config(
        conn_max_age=600,
    )
}


STATIC_ROOT = Path(BASE_DIR, "static")


CSRF_COOKIE_SECURE = True
CSRF_COOKIE_HTTPONLY = True

SECURE_HSTS_SECONDS = 60 * 60 * 24 * 7 * 52  # one year
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_SSL_REDIRECT = True  # !важно
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

SESSION_COOKIE_SECURE = True  # !важно


CSRF_TRUSTED_ORIGINS = [
    os.environ.get('ALLOWED_HOSTS')
]
