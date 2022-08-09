from app.utils import root_directory
from app.bootstrap.config import Config

SECRET_KEY = Config.get('main.secret_key')
ALLOWED_HOSTS = ['*']

# Note the ROOT_URLCONF value, changed from the default
ROOT_URLCONF = 'app.bootstrap.entrypoint_urls'
WSGI_APPLICATION = 'app.bootstrap.wsgi.application'

# Remove unused built-in apps
# Notably admin and auth apps
# We don't use django's authentication system, in favour of our own custom
# authentication + authurization engine
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

# This disables the automatic redirect of requests not ending with a slash, which causes loss of POST body
APPEND_SLASH = False

# display all messages (above the given level, and 0 is the min level)
MESSAGE_LEVEL = 0

SESSION_ENGINE = 'django.contrib.sessions.backends.file'
SESSION_FILE_PATH = root_directory(['storage', 'sessions'], create_missing=True)

STATIC_URL = '/static/'
STATIC_ROOT = root_directory(['storage', 'assets'], create_missing=True) + '/'  # target for collectstatic ( the ending '/' is required )

MEDIA_ROOT = root_directory(['storage', 'media'], create_missing=True) + '/'

# Places to look for static assets
# This is currently an API, so no static stuff
STATICFILES_DIRS = []

# For convinience, currently allow all IPs
INTERNAL_IPS = ['*']

# Even though CSRF is not used currently, it is still nice to have setup
CSRF_FAILURE_VIEW = f'{ROOT_URLCONF}.handler_csrf_failure'

# ========================================== Third Party ==========================================

REST_FRAMEWORK = {
    # Turn off django-rest-framework authorizationn since we will be implementing our own.
    'UNAUTHENTICATED_USER': None,
    'DEFAULT_AUTHENTICATION_CLASSES': [],
    'DEFAULT_PERMISSION_CLASSES': [],

    # Default only json responses
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer'
    ]
}

# CORS settings
CORS_PREFLIGHT_MAX_AGE = 0
CORS_ALLOW_CREDENTIALS = True

CORS_ALLOWED_ORIGIN_REGEXES = [
    # allow CORS on all ports of localhost (including no port)
    r"^http:\/\/localhost(:[0-9]+)?$",
    # allow CORS on all ip addrs of form 127.x.y.z[:port]
    r"^http:\/\/127\.[0-9]+\.[0-9]+\.[0-9]+(:[0-9]+)?$" 
]

