from django.http import HttpRequest, JsonResponse

from app.exceptions import (
    response_exception,

    ApiException,
    HttpException,
)

class ExceptionHandlerMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, req):
        return self.get_response(req)

    def process_exception(self, request: HttpRequest, exp: Exception):

        if isinstance(exp, ApiException):
            response = JsonResponse({
                'type': 'error',
                'message': exp.msg, 
                'payload': exp.data
            }, status=exp.code)

            return response

        # Note the ordering of if-elif statements. ApiException itself is a subclass of HttpException
        elif isinstance(exp, HttpException):
            return response_exception(request, exp)

        return None
