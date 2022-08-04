import os
import re

from django.urls import path, re_path, include, reverse
from django.shortcuts import redirect
# from django.conf.urls import url

from app.bootstrap.config import Config
from app.exceptions import (
    response_exception,
    HttpException,
    HTTPStatus
)

def _specialize_exception_handler(exception: HttpException):
    def f(request, *args, **kwargs):
        return response_exception(request, exception)

    return f


# These handlers only take effect when running with DEBUG=False (production)
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
else:
    # If we are in debug mode then django automatically serves static files
    # When debug mode is turned off and force_serve_static_files is True then
    # we explicitly serve static files here 
    if Config.get_bool('runtime.force_serve_static_files'):
        # from django.contrib.staticfiles.urls import staticfiles_urlpatterns
        # urlpatterns += staticfiles_urlpatterns()
        
        ## Well turns out the above code doesn't work in production as staticfiles_urlpatterns() checks for DEBUG being true
        ## so TODO: replace this line with a (WhiteNoise) library which serves static files even with DEBUG turned off
        ## Meanwhile the following customized staticfiles_urlpatterns() hack should work

        from django.conf import settings
        from django.contrib.staticfiles.views import serve
        prefix = settings.STATIC_URL
        urlpatterns += [re_path(r'^%s(?P<path>.*)$' % re.escape(prefix.lstrip('/')), serve)]





