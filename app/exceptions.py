from typing import TYPE_CHECKING
import copy

from http import HTTPStatus

from django.http import HttpRequest
    
from django.shortcuts import render

class HttpException(Exception):
    def __init__(self, code, msg):
        self.code = code
        self.msg = msg

    @classmethod
    def from_http_status_code(cls, status: HTTPStatus):
        return cls(code=status.value, msg=status.phrase)

    def __repr__(self):
        return f"<HttpException: {self.code} ({self.msg})>"

# --------------------------------------------------

def response_exception(request: HttpRequest, exp: HttpException):
    return render(request, 'main/errors/generic.html', {
        "code": exp.code,
        "msg": exp.msg
    }, status=exp.code)

# --------------------------------------------------

class ApiException(HttpException):
    def __init__(self, code=500, msg=None, data=None):
        super().__init__(code, msg)
        self.data = data

    # Currently only copying with message and data is allowed. That is because it doesn't make sense to
    # change the status code if you are "copying" in the first place .
    def copy_with(self, msg=None, data=None):
        return ApiException(
            msg=msg or copy.deepcopy(self.msg),
            code=self.code,
            data=data or copy.deepcopy(self.data)
        )

    @classmethod
    def from_http_status_code(cls, status: HTTPStatus, data=None):
        return cls(code=status.value, msg=f"HTTP {status.value} - {status.phrase}", data=data);


class ApiExceptionCollection:
    NotFound = ApiException.from_http_status_code(HTTPStatus.NOT_FOUND)
    BadRequest = ApiException.from_http_status_code(HTTPStatus.BAD_REQUEST)
    UnprocessableEntity = ApiException.from_http_status_code(HTTPStatus.UNPROCESSABLE_ENTITY)
