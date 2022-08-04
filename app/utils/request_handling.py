from typing import cast
from django.http import HttpRequest, QueryDict
from django.shortcuts import redirect


def redirect_back(req: HttpRequest, default_url='/'):
    return redirect(req.META.get('HTTP_REFERER', default_url))
