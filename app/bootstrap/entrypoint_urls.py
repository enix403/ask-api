import os
import re

from django.urls import path, re_path, include, reverse
from django.shortcuts import redirect

from app.bootstrap.config import Config
from app.exceptions import (
    response_exception,
    HttpException,
    ApiException,
    HTTPStatus
)


# Create a handler that just retuns the given exception
def _specialize_exception_handler(exception: HttpException):
    def f(request, *args, **kwargs):
        return response_exception(request, exception)

    return f


# These handlers only take effect when running with DEBUG=False
# See https://docs.djangoproject.com/en/4.1/topics/http/views/#customizing-error-views
handler400              = _specialize_exception_handler(HttpException.from_http_status_code(HTTPStatus.BAD_REQUEST))
handler403              = _specialize_exception_handler(HttpException.from_http_status_code(HTTPStatus.FORBIDDEN))
handler404              = _specialize_exception_handler(HttpException.from_http_status_code(HTTPStatus.NOT_FOUND))
handler500              = _specialize_exception_handler(HttpException.from_http_status_code(HTTPStatus.INTERNAL_SERVER_ERROR))
handler_csrf_failure    = _specialize_exception_handler(HttpException.from_http_status_code(HTTPStatus.FORBIDDEN))

urlpatterns = [
    path("", lambda _req: redirect('/api/v1/')),
    path("api/", include("app.routes")),
]

if Config.get_bool('runtime.debug'):
    try:
        # urlpatterns += [url(r'^silk/', include('silk.urls', namespace='silk'))]
        import debug_toolbar
        urlpatterns += [path('__debug__/', include(debug_toolbar.urls))]
    except:
        # TODO: log error
        pass

