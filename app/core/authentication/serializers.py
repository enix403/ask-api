import re

from rest_framework import serializers as s
from rest_framework.exceptions import ValidationError


from app.utils.qs import qs_exists, qs_filter
from app.exceptions import ApiExceptionCollection
from app.models.auth import AppUser


class EmailValidator:

    EMAIL_REGEX = re.compile(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)")

    def __init__(self, required=True):
        self.required = required

    def __call__(self, value):
        is_none = value is None
        if self.required:
            if is_none:
                raise ValidationError("Invalid email", code='invalid_email_null')
        elif is_none:
            return

        if not re.fullmatch(self.EMAIL_REGEX, value):
            raise ValidationError("Invalid email format", code='invalid_email')

        

class UniqueFieldValidator:
    _s_message = "This field must be unique."
    _s_message_required = "This field must be unique and non-null"

    def __init__(self, queryset, message=None, model_field=None, required=True):
        self.queryset = queryset
        self.message = message
        self.model_field = model_field
        self.required = required

    def __call__(self, value):
        if self.required and value is None:
            raise ValidationError(
                self.message or self._s_message_required, code='create_unique_null')

        model_field = self.model_field or "id"

        if qs_exists(qs_filter(self.queryset, **{ model_field: value })):
            raise ValidationError(
                self.message or self._s_message, code='create_unique')


class ApiSerializer(s.Serializer):
    def validate_api(self):
        """ Raise ApiException on failed validation """
        if not self.is_valid():
            raise ApiExceptionCollection.UnprocessableEntity.copy_with(
                msg="Invalid form values",
                data=self.errors
            )
        return self


class UserProfileSerializer(ApiSerializer):
    first_name = s.CharField(max_length=250)
    last_name = s.CharField(max_length=250)

    phone_number = s.CharField(max_length=100)
    post_code = s.CharField(max_length=50)
    address_line_1 = s.CharField(max_length=250)
    address_line_2 = s.CharField(max_length=250)
    age = s.IntegerField(min_value=1)
    about_me = s.CharField(allow_blank=True)

    profile_pic_handle = s.CharField(required=False, allow_null=True)


class CreateUserSerializer(UserProfileSerializer):
    username = s.CharField(
        max_length=250,
        validators=[UniqueFieldValidator(
            message="Username already taken",
            queryset=AppUser.objects.all(),
            model_field="username"
        )]
    )
    email = s.CharField(
        max_length=250,
        validators=[
            EmailValidator(),
            UniqueFieldValidator(message="Email already taken", queryset=AppUser.objects.all(), model_field="email")
        ]
    )
    password = s.CharField(min_length=3)


class UpdateUserCredSerializer(ApiSerializer):

    def __init__(self, user: AppUser, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user

    username = s.CharField(max_length=250, allow_null=True)
    email = s.CharField(max_length=250, validators=[EmailValidator(required=False)], allow_null=True)

    def validate(self, data):
        username = data.get('username', None)
        email = data.get('email', None)

        if username is not None and username != self.user.username:
            UniqueFieldValidator(
                message="Username already taken",
                queryset=AppUser.objects.all(),
                model_field="username"
            )(username)

        if email is not None and email != self.user.email:
            UniqueFieldValidator(
                message="Email already taken",
                queryset=AppUser.objects.all(),
                model_field="email"
            )(email)

        return data


class LoginSerializer(ApiSerializer):
    username = s.CharField()
    password = s.CharField()


class UserProfileView(UserProfileSerializer):
    username = s.CharField()
    email = s.CharField()
    profile_pic_location = s.CharField()


class UpdatePasswordSerializer(ApiSerializer):
    password = s.CharField(min_length=3)

    def validate(self, data):
        # TODO: Add password strength check
        return data
