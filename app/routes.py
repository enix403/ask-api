from django.urls import re_path, path, include
# from django.http import JsonResponse

from app.communication import ApiRequest, ApiResponse, api_view

from app.core.authentication.apiviews import (
    upload_picture,
    signup_user,
    login_user,
    user_profile,
)

@api_view()
def not_implemented(_):
    return ApiResponse({'error': 'Cannot GET /'}, status=400)

@api_view()
def v1_index(_):
    return ApiResponse('Welcome to API-v1')

urlpatterns = [
    path("", not_implemented),
    path('v1/', include([
        path("", v1_index),

        path('auth/signup/', signup_user),
        path('user/upload-picture/', upload_picture),
        path('auth/login/', login_user),
        path('user/profile/', user_profile),
    ]))
]