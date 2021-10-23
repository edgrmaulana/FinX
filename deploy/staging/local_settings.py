BASE_URL = "https://account.finx.nikici.com"
DEBUG = True
PRODUCTION = False

# database configuration
DATABASES = {
    "default": {
        "ENGINE": "django.contrib.gis.db.backends.postgis",
        "NAME": "finx_account_db",
        "USER": "sagara",
        "PASSWORD": "barakadut1234",
        "HOST": "127.0.0.1",
        "PORT": "5432",
        "TEST": {"NAME": "finx_account_test_db"},
    }
}

# Email
EMAIL_HOST = "smtp.zoho.com"
EMAIL_PORT = 587
EMAIL_HOST_USER = "arif@sagara.asia"
EMAIL_HOST_PASSWORD = "Computer7!"
FROM_EMAIL = "Sagara FIntech <arif@sagara.asia>"
EMAIL_USE_TLS = True

# SMS Provider
NEXMO_API_KEY = "48a6d152"
NEXMO_API_SECRET = "Zb9YDrbduuJ4zfq3"

# Cors
CORS_ORIGIN_ALLOW_ALL = True

# social google auth
SOCIAL_AUTH_REDIRECT_IS_HTTPS = True
SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = (
    "488082588111-2iep29f8esbgpv7fpgpknqtnilpu7rc3.apps.googleusercontent.com"
)
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = "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"

# Define SOCIAL_AUTH_GOOGLE_OAUTH2_SCOPE to get extra permissions from Google.
SOCIAL_AUTH_GOOGLE_OAUTH2_SCOPE = [
    "https://www.googleapis.com/auth/userinfo.email",
    "https://www.googleapis.com/auth/userinfo.profile",
]
