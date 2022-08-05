from typing import Optional, Any
from django.db.models.fields.json import KeyTransformExact
from rest_framework import serializers as s
from rest_framework.decorators import api_view
from app.exceptions import ApiExceptionCollection

from auth_core import AclContext, Allow

from app.models.auth import AppUser
from app.communication import api_view, ApiRequest, ApiResponse

from .keystore import KeyStore
from .engine import TR, require, ContextGenerator

class CreateSerializer(s.Serializer):
    pass

class CreateUserSerializer(CreateSerializer):

    class KMeta:
        ref_model = AppUser

    username = s.CharField(max_length=250)
    password = s.CharField()
    email = s.CharField(max_length=250)

    first_name = s.CharField(max_length=250)
    last_name = s.CharField(max_length=250)

    phone_number = s.CharField(max_length=100)
    post_code = s.CharField(max_length=50)
    address_line_1 = s.CharField(max_length=250)
    address_line_2 = s.CharField(max_length=250)
    age = s.IntegerField(min_value=1)
    about_me = s.CharField()

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

    user.save()

    return ApiResponse.make_success(
        "User signed up successfully",
        {
            "api_key": serialized_key
        }
    )
