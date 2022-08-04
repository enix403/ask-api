import os
from app.utils import resolve_root

from app.bootstrap.settings.components.base import (
    INSTALLED_APPS,
    REST_FRAMEWORK
)
from app.bootstrap.settings.components.middleware import (
    MIDDLEWARE
)

DEBUG = True
# DEBUG = False

INSTALLED_APPS.extend([
    'debug_toolbar',
    'django_extensions',
])

MIDDLEWARE.extend([
    'debug_toolbar.middleware.DebugToolbarMiddleware',
])

TEMPLATE_DEBUG = True

SHELL_PLUS = "plain"
X_ENABLE_DEBUGBAR = True

DEBUG_TOOLBAR_CONFIG = {
    'SHOW_TOOLBAR_CALLBACK': lambda _: X_ENABLE_DEBUGBAR,
}

# ========================================== Third Party ==========================================

REST_FRAMEWORK = {
    **REST_FRAMEWORK,
    'DEFAULT_RENDERER_CLASSES': REST_FRAMEWORK['DEFAULT_RENDERER_CLASSES'] + [
        'rest_framework.renderers.BrowsableAPIRenderer',
    ]
}
