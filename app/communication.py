from django.http.request import QueryDict
from rest_framework.request import Request as _Request
from rest_framework.response import Response as _Response

# Re-exports
from rest_framework.decorators import api_view
from django.http import HttpRequest, HttpResponse

class ApiRequest(_Request):
    COOKIES: dict[str, str]
    content_type: str
    method: str
    data: QueryDict

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