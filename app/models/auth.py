from typing import Any, Optional

from app.utils.passlib_hash import pbkdf2_sha256

from . import fields as f
from .core import BaseModel

class TimeStampedModel(f.models.Model):
    class Meta:
        abstract = True

    # See https://docs.djangoproject.com/en/4.1/ref/models/fields/#datefield
    created_at = f.DateTimeField(auto_now_add=True)
    updated_at = f.DateTimeField(auto_now=True)


class StatusTrackedModel(f.models.Model):
    class Meta:
        abstract = True

    is_active = f.PositiveTinyIntegerField(default=1)
    is_deleted = f.PositiveTinyIntegerField(default=0)



# ------------------------------------------------

class ProfilePicture(BaseModel['ProfilePicture']):
    class Meta:
        db_table = 'k_profile_pics'

    name = f.CharField(max_length=250, unique=True, db_index=True)
    location = f.CharField(max_length=250)

    @staticmethod
    def handle_of(profile: Optional['ProfilePicture']):
        if profile is None:
            return None

        # Might use a different field as handle in the future
        return profile.name

    @staticmethod
    def from_handle(handle: Any) -> Optional['ProfilePicture']:
        if handle is None:
            return None

        return ProfilePicture.objects.filter(name=handle).first()


class UserProfileMixin(f.models.Model):
    class Meta:
        abstract = True

    phone_number = f.CharField(max_length=100)
    post_code = f.CharField(max_length=50)
    address_line_1 = f.CharField(max_length=250)
    address_line_2 = f.CharField(max_length=250)
    age = f.IntegerField()
    about_me = f.TextField()
    profile_picture = f.make_fk(ProfilePicture, column_name='pic_id', null=True)


class AppUser(BaseModel['AppUser'], TimeStampedModel, StatusTrackedModel, UserProfileMixin):
    class Meta:
        db_table = 'k_app_users'

    # Might wanna store sort of "api keys history" in the future. So `current_api_key` makes more sense
    # For now it stores the actual key, needed for a lookup. In the future it should be updated to
    # hold the hash
    current_api_key = f.CharField(max_length=250, db_index=True)

    username = f.CharField(max_length=250)
    password_hash = f.CharField(max_length=250)

    first_name = f.CharField(max_length=250)
    last_name = f.CharField(max_length=250)

    email = f.CharField(max_length=250)

    @classmethod
    def make(cls, username, password):
        user = cls()
        user.username = username
        user.set_password(password)
        return user

    def set_password(self, password):
        self.password_hash = pbkdf2_sha256.using(rounds=29000, salt_size=16).hash(password)

    def verify_password(self, password):
        return pbkdf2_sha256.verify(password, self.password_hash)
