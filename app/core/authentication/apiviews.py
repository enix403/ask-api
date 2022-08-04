from typing import Optional
# app.core.authentication.apiviews

from auth_core import AclContext, Allow

from app.communication import api_view, ApiRequest, ApiResponse

from .engine import TR, require, ContextGenerator


@api_view(['GET', 'POST'])
def signup_user(request: ApiRequest) -> ApiResponse:
    return ApiResponse({
        'type': 'success',
        'msg': f'User signed up successfully',
        'payload': { 'here': 'we', 'go': 2324 }
    })