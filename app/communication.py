from typing import Optional
from django.http.request import QueryDict
from django.core.files.uploadedfile import UploadedFile
from django.utils.datastructures import MultiValueDict

from rest_framework.request import Request as _Request
from rest_framework.response import Response as _Response

# Re-exports
from rest_framework.decorators import api_view
from django.http import HttpRequest, HttpResponse, JsonResponse

from app.models.auth import AppUser

class ApiRequest(_Request):
    COOKIES: dict[str, str]
    FILES: MultiValueDict[str, UploadedFile]
    content_type: str
    method: str
    data: QueryDict
    user: Optional[AppUser]

# It looks ugly having 'import rest_framework.response.Response' everywhere,
# plus there is already an `ApiRequest` class anyway, so why not give it a friend
class ApiResponse(_Response):
    @classmethod
    def make_success(cls, msg="", payload=None):
        return cls({
            'type': 'success',
            'message': msg,
            'payload': payload
        })

    @classmethod
    def make_error(cls, msg="", payload=None):
        return cls({
            'type': 'error',
            'message': msg,
            'payload': payload
        })