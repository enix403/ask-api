import re
import uuid

from pathlib import Path
from http import HTTPStatus
from typing import Optional, Any

from rest_framework import serializers as s
from rest_framework.decorators import api_view
from rest_framework.exceptions import ValidationError

from django.conf import settings

from auth_core import AclContext

from app.app_paths import AppPaths
from app.utils.qs import qs_exists, qs_filter
from app.models.auth import AppUser, ProfilePicture
from app.exceptions import ApiException, ApiExceptionCollection
from app.communication import (
    ApiRequest,
    ApiResponse,
)

from .keystore import KeyStore
from .engine import TR, require, FixedContextGenerator


class CreateSerializer(s.Serializer):
    pass


class UniqueFieldValidator:
    """
    Validator that corresponds to `unique=True` on a model field.

    Should be applied to an individual field on the serializer.
    """

    message = "This field must be unique."

    def __init__(self, queryset, message=None, model_field=None):
        self.queryset = queryset
        self.message = message or self.message
        self.model_field = model_field


    def __call__(self, value):

        model_field = self.model_field or "id"

        if qs_exists(qs_filter(self.queryset, **{ model_field: value })):
            raise ValidationError(self.message, code='create_unique')


# PROFILE_PICS_STORAGE = Path(settings.MEDIA_ROOT) / 'profile_pics'
# PROFILE_PICS_STORAGE.mkdir(parents=True, exist_ok=True)

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

    return ApiResponse.make_success(payload={'handle': record.name})

EMAIL_REGEX = re.compile(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)")
def validate_email(email):
    if not re.fullmatch(EMAIL_REGEX, email):
        raise ValidationError("Invalid email format", code='invalid_email')

class CreateUserSerializer(CreateSerializer):

    class KMeta:
        ref_model = AppUser

    username = s.CharField(
        max_length=250,
        validators=[UniqueFieldValidator(
            message="Username already taken",
            queryset=AppUser.objects.all(),
            model_field="username"
        )]
    )
    password = s.CharField()
    email = s.CharField(
        max_length=250,
        validators=[
            validate_email,
            UniqueFieldValidator(message="Email already taken", queryset=AppUser.objects.all(), model_field="email")
        ]
    )

    first_name = s.CharField(max_length=250)
    last_name = s.CharField(max_length=250)

    phone_number = s.CharField(max_length=100)
    post_code = s.CharField(max_length=50)
    address_line_1 = s.CharField(max_length=250)
    address_line_2 = s.CharField(max_length=250)
    age = s.IntegerField(min_value=1)
    about_me = s.CharField()

    profile_pic_handle = s.CharField(required=False, allow_null=True)


@api_view(['POST'])
def signup_user(request: ApiRequest) -> ApiResponse:

    ss = CreateUserSerializer(data=request.data) # type: ignore

    if not ss.is_valid():
        raise ApiExceptionCollection.UnprocessableEntity.copy_with(
            msg="Invalid form values",
            data=ss.errors
        )

    data = ss.validated_data # type: dict[Any, Any]

    user = AppUser.make(data.get('username'), data.get('password'))

    user.first_name = data['first_name']
    user.last_name = data['last_name']
    user.email = data['email']

    user.phone_number = data['phone_number']
    user.post_code = data['post_code']
    user.address_line_1 = data['address_line_1']
    user.address_line_2 = data['address_line_2']
    user.age = data['age']
    user.about_me = data['about_me']

    user_key = KeyStore.generate_fresh()
    serialized_key = KeyStore.serialize_user(user_key)

    user.current_api_key = serialized_key

    user.profile_picture = None # type: ignore
    pic_handle = data.get('profile_pic_handle', None)
    if pic_handle is not None:
        try:
            user.profile_picture = ProfilePicture.objects.get(name=pic_handle)
        except:
            # TODO: Do not silently fail like this when invalid picture handle is provided
            pass

    user.save()

    return ApiResponse.make_success(
        msg="User signed up successfully",
        payload={
            "api_key": serialized_key
        }
    )


class LoginSerializer(s.Serializer):
    username = s.CharField()
    password = s.CharField()


login_failure_execption = ApiException(HTTPStatus.UNAUTHORIZED, msg="Invalid username or password")

@api_view(['POST'])
def login_user(request: ApiRequest) -> ApiResponse:

    ss = LoginSerializer(data=request.data) # type: ignore

    if not ss.is_valid():
        raise ApiExceptionCollection.UnprocessableEntity.copy_with(
            msg="Invalid form values",
            data=ss.errors
        )

    data = ss.validated_data # type: dict[Any, Any]

    try:
        user = AppUser.objects.filter(username=data['username']).get()
    except AppUser.DoesNotExist:
        raise login_failure_execption

    if not user.verify_password(data['password']):
        raise login_failure_execption

    return ApiResponse.make_success(
        msg="Login successful",
        payload={
            "api_key": user.current_api_key
        }
    )


@api_view(["GET"])
@require(
    'access',
    FixedContextGenerator(AclContext.trait_singular(TR.Authenticated))
)
def user_profile(request: ApiRequest) -> ApiResponse:
    return ApiResponse.make_success(payload="You got it")