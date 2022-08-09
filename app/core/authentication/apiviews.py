import uuid

from pathlib import Path
from http import HTTPStatus
from typing import Optional, Any, cast

from rest_framework.decorators import api_view

from auth_core import AclContext

from app.app_paths import AppPaths
from app.models.auth import AppUser, ProfilePicture
from app.exceptions import ApiException
from app.communication import (
    ApiRequest,
    ApiResponse,
)

from .keystore import KeyStore
from .engine import TR, require, FixedContextGenerator
from .serializers import (
    UserProfileSerializer,
    CreateUserSerializer,
    LoginSerializer,
    UserProfileView,
    UpdateUserCredSerializer,
    UpdatePasswordSerializer
)


def extract_user(request: ApiRequest) -> AppUser:
    return cast(AppUser, request.user)


@api_view(['POST'])
def upload_picture(request: ApiRequest) -> ApiResponse:
    # TODO: Protect this route with at-least some app-level authorization (not user-level) to prevent spamming/DOS

    file = request.FILES['image'] # type: ignore

    extension = Path(file.name).suffix

    name = str(uuid.uuid4())
    location = name + extension

    record = ProfilePicture()
    record.name = name
    record.location = location

    try:
        record.save()
    except:
        raise ApiException(
            code=HTTPStatus.INTERNAL_SERVER_ERROR, msg="Failed to upload image. Try again later")

    with open(str(AppPaths.profile_pics() / location), 'wb+') as destination:
        for chunk in file.chunks():
            destination.write(chunk)

    return ApiResponse.make_success(payload={'handle': ProfilePicture.handle_of(record)})




@api_view(['POST'])
def signup_user(request: ApiRequest) -> ApiResponse:

    ss = CreateUserSerializer(data=request.data) # type: ignore
    ss.validate_api()

    data = ss.validated_data # type: dict[Any, Any]

    user = AppUser.make(data.get('username'), data.get('password'))

    user_key = KeyStore.generate_fresh()
    serialized_key = KeyStore.serialize_user(user_key)

    user.current_api_key = serialized_key

    user.first_name = data['first_name']
    user.last_name = data['last_name']
    user.email = data['email']

    user.phone_number = data['phone_number']
    user.post_code = data['post_code']
    user.address_line_1 = data['address_line_1']
    user.address_line_2 = data['address_line_2']
    user.age = data['age']
    user.about_me = data['about_me']

    pic_handle = data.get('profile_pic_handle', None)
    user.profile_picture = ProfilePicture.from_handle(pic_handle) # type: ignore

    user.save()

    return ApiResponse.make_success(
        msg="User signed up successfully",
        payload={
            "api_key": serialized_key
        }
    )


# Instantiate most used exceptions for performance
login_failure_execption = ApiException(HTTPStatus.UNAUTHORIZED, msg="Invalid username or password")
user_inactive_execption = ApiException(HTTPStatus.UNAUTHORIZED, msg="User's account is not active")

@api_view(['POST'])
def login_user(request: ApiRequest) -> ApiResponse:

    ss = LoginSerializer(data=request.data) # type: ignore
    ss.validate_api()

    data = ss.validated_data # type: dict[Any, Any]

    try:
        user = AppUser.objects.filter(username=data['username']).get()
    except AppUser.DoesNotExist:
        raise login_failure_execption

    if user.is_deleted == 1 or not user.verify_password(data['password']):
        raise login_failure_execption

    if user.is_active == 0:
        raise user_inactive_execption

    return ApiResponse.make_success(
        msg="Login successful",
        payload={
            "api_key": user.current_api_key
        }
    )



ctx_authenticated = AclContext.trait_singular(TR.Authenticated)


@api_view(["GET"])
@require('access', FixedContextGenerator(ctx_authenticated))
def user_profile(request: ApiRequest) -> ApiResponse:
    user = extract_user(request)

    pf = user.profile_picture

    ss = UserProfileView({
        "username": user.username,
        "email": user.email,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "phone_number": user.phone_number,
        "post_code": user.post_code,
        "address_line_1": user.address_line_1,
        "address_line_2": user.address_line_2,
        "age": user.age,
        "about_me": user.about_me,
        "profile_pic_handle": ProfilePicture.handle_of(pf),
        "profile_pic_location": None if pf is None else pf.location,
    }) # type: ignore


    return ApiResponse.make_success(payload=ss.data)



@api_view(["POST"])
@require('access', FixedContextGenerator(ctx_authenticated))
def user_profile_update(request: ApiRequest) -> ApiResponse:
    user = extract_user(request)

    ss = UserProfileSerializer(data=request.data) # type: ignore
    ss.validate_api()

    data = ss.validated_data

    user.first_name = data['first_name']
    user.last_name = data['last_name']

    user.phone_number = data['phone_number']
    user.post_code = data['post_code']
    user.address_line_1 = data['address_line_1']
    user.address_line_2 = data['address_line_2']
    user.age = data['age']
    user.about_me = data['about_me']

    pic_handle = data.get('profile_pic_handle', None)
    user.profile_picture = ProfilePicture.from_handle(pic_handle) # type: ignore

    user.save()

    data['profile_pic_handle'] = ProfilePicture.handle_of(user.profile_picture)

    return ApiResponse.make_success(payload=data)


@api_view(["POST"])
@require('access', FixedContextGenerator(ctx_authenticated))
def user_cred_update(request: ApiRequest) -> ApiResponse:
    user = extract_user(request)

    ss = UpdateUserCredSerializer(user=user, data=request.data) # type: ignore
    ss.validate_api()

    data = ss.validated_data

    username = data.get('username', None)
    email = data.get('email', None)

    if username is not None:
        user.username = username

    if email is not None:
        user.email = email

    user.save()

    return ApiResponse.make_success(payload=ss.validated_data)


@api_view(["POST"])
@require('access', FixedContextGenerator(ctx_authenticated))
def user_password_update(request: ApiRequest) -> ApiResponse:
    ss = UpdatePasswordSerializer(data=request.data).validate_api() # type: ignore

    user = extract_user(request)
    user.set_password(ss.validated_data['password'])

    user.save()

    return ApiResponse.make_success(msg="Password updated successfully")