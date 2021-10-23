BASE_URL = "http://localhost:8000"
DEBUG = True
PRODUCTION = False

# database configuration
DATABASES = {
    "default": {
        "ENGINE": "django.contrib.gis.db.backends.postgis",
        "NAME": "your_db_name",
        "USER": "postgres",
        "PASSWORD": "your_password",
        "HOST": "your_host",
        "PORT": "5432",
        "TEST": {"NAME": "your_db_name"},
    }
}

# Email
EMAIL_HOST = "smtp.zoho.com"
EMAIL_PORT = 587
EMAIL_HOST_USER = "askme"
EMAIL_HOST_PASSWORD = "askme"
FROM_EMAIL = "askme"
EMAIL_USE_TLS = True

# Cors
CORS_ORIGIN_ALLOW_ALL = True

# social google auth
SOCIAL_AUTH_REDIRECT_IS_HTTPS = True
SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = "askme"
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = "askme"

# Define SOCIAL_AUTH_GOOGLE_OAUTH2_SCOPE to get extra permissions from Google.
SOCIAL_AUTH_GOOGLE_OAUTH2_SCOPE = [
    "https://www.googleapis.com/auth/userinfo.email",
    "https://www.googleapis.com/auth/userinfo.profile",
]
