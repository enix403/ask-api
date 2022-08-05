from app.utils import root_directory
from app.bootstrap.config import Config

SECRET_KEY = Config.get('main.secret_key')
ALLOWED_HOSTS = ['*']

ROOT_URLCONF = 'app.bootstrap.entrypoint_urls'
WSGI_APPLICATION = 'app.bootstrap.wsgi.application'

INSTALLED_APPS = [
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'rest_framework',
    'corsheaders',
    'app.appconfig.AppConfig',
]

LANGUAGE_CODE = 'en-us'
USE_I18N = False
USE_L10N = False
TIME_ZONE = 'UTC'
USE_TZ = True

APPEND_SLASH = False

MESSAGE_LEVEL = 0 # display all messages (above the given level, and 0 is the min level)

SESSION_ENGINE = 'django.contrib.sessions.backends.file'
SESSION_FILE_PATH = root_directory(['storage', 'sessions'], create_missing=True)

STATIC_URL = '/static/'
STATIC_ROOT = root_directory(['storage', 'assets'], create_missing=True) + '/'  # target for collectstatic ( the ending '/' is required )

MEDIA_ROOT = root_directory(['storage', 'media'], create_missing=True) + '/'

# places to look for static assets
STATICFILES_DIRS = []

INTERNAL_IPS = ['*']

# ========================================== Third Party ==========================================

REST_FRAMEWORK = {
    'UNAUTHENTICATED_USER': None,
    'DEFAULT_AUTHENTICATION_CLASSES': [],
    'DEFAULT_PERMISSION_CLASSES': [],
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer'
    ]
}


CORS_PREFLIGHT_MAX_AGE = 0
CORS_ALLOW_CREDENTIALS = True

CORS_ALLOWED_ORIGIN_REGEXES = [
    # allow CORS on all ports of localhost (including no port)
    r"^http:\/\/localhost(:[0-9]+)?$",
    # allow CORS on all ip addrs of form 127.x.y.z[:port]
    r"^http:\/\/127\.[0-9]+\.[0-9]+\.[0-9]+(:[0-9]+)?$" 
]

