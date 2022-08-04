from django.urls import re_path, path, include
# from django.http import JsonResponse

from app.communication import ApiRequest, ApiResponse, api_view

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
    ]))
]