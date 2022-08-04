from typing import cast
import datetime
from app.core.sections.context import SectionContext
from app.core.manage.context import CollegeContext, StationContext

from rest_framework.decorators import api_view

from app.models import College
from authzx.helpers import make_ctx_require_all_traits
from app.core.authentication.traits import TR
from app.typehints import ApiRequest, ApiResponse
from app.exceptions import ApiException
from app.models import AppUser

from . import permissions
from .token import TokenDecodeResult, decode_token, new_access_token, new_ref_token

REFRESH_TOKEN_COOKIE_NAME = 'ref_token'

@api_view(['POST'])
def login(request: ApiRequest) -> ApiResponse:
    username = request.data.get('username', None)
    password = request.data.get('password', None)

    failure_exp = ApiException("Invalid username or password", data={'access': '', 'refresh_token_id': ''})

    if not username or not password:
        raise failure_exp

    try:
        user = AppUser.objects.filter(username=username).get()
    except AppUser.DoesNotExist:
        raise failure_exp

    if not user.verify_password(password):
        raise failure_exp

    access_token = new_access_token(user.pk)
    expires_at = datetime.datetime.utcnow() + datetime.timedelta(days=20)
    ref_token, ref_token_id = new_ref_token(user.pk, expires_at)

    response = ApiResponse({
        'type': 'success',
        'msg': 'Login successful',
        'payload': {
            'access': access_token,
            'refresh_token_id': ref_token_id 
        }
    })

    response.set_cookie(
        REFRESH_TOKEN_COOKIE_NAME, ref_token, 
        expires=expires_at, 
        httponly=True,
        samesite='None',
        secure=False,
        path='/'
    )
    return response

@api_view(['POST'])
def logout(request: ApiRequest) -> ApiResponse:
    response = ApiResponse({
        'type': 'success',
        'msg': '',
    })

    response.delete_cookie(REFRESH_TOKEN_COOKIE_NAME, path='/') # Path is required
    return response

@api_view(['POST'])
def refresh_access_token(request: ApiRequest) -> ApiResponse:
    ref_token = request.COOKIES.get(REFRESH_TOKEN_COOKIE_NAME, '')
    decode_result = decode_token(ref_token)
    data = {'access': ''}

    if not decode_result.success:
        if decode_result.fail_reason == TokenDecodeResult.FailureReason.EXPIRED:
            raise ApiException("Expired refresh token. Please login again", data=data)
        else:
            raise ApiException("Invalid refresh token. Please login again", data=data)

    payload = decode_result.payload;

    if payload['tk_type'] != 'ref':
        raise ApiException("Invalid refresh token. Please login again", data=data)

    ref_token_id = request.data.get('refresh_token_id', '')
    if payload['jti'] != ref_token_id:
        raise ApiException("CSRF Failure. Please login again", data=data)

    access_token = new_access_token(payload['userid'])
    data['access'] = access_token
    return ApiResponse({
        'type': 'success',
        'msg': 'Token refresh successful',
        'payload': data
    })



_authenticated_context = make_ctx_require_all_traits(TR.Authenticated)
@api_view(['GET'])
def get_user_info(request: ApiRequest) -> ApiResponse:
    gate = permissions.ApiPermissionGate(request)
    gate.require('access', _authenticated_context)

    user = cast(AppUser, gate.get_user())
    try:
        college = College.objects.filter(pk=user.college_id).get()
        clg_name = college.name
        clg_id = college.pk
    except:
        clg_name = ''
        clg_id = None


    return ApiResponse({
        'type': 'success',
        'msg': '',
        'payload': {
            'info': {
                'name': user.name,
                'username': user.username,
                'authrole': user.auth_role,
                'staffrole': user.staff_role,
                'college': {
                    'id': clg_id,
                    'name': clg_name,
                }
            },
            'permissions': {
                'colleges': gate.all_permissions(CollegeContext.generate(request)),
                'station': gate.all_permissions(StationContext.generate(request)),
                'sections': gate.all_permissions(SectionContext(user.college_id).generate(None))
            }
        }
    })
