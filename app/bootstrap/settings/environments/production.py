from app.bootstrap.settings.components.base import (
    ROOT_URLCONF
)

DEBUG = False
CSRF_FAILURE_VIEW = f'{ROOT_URLCONF}.handler_csrf_failure'