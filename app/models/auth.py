from django.db import models

from app.utils.passlib_hash import pbkdf2_sha256

from . import fields
from .core import BaseModel

class AppUser(BaseModel['AppUser']):
    class Meta:
        db_table = 'spl1_users'

    name = models.CharField(max_length=25)
    username = models.CharField(max_length=30)
    password_hash = models.CharField(max_length=200)
    invalidate = fields.PositiveTinyIntegerField(default=0)

    @classmethod
    def make(cls, name, username, password):
        user = cls()
        user.name = name
        user.username = username
        user.password_hash = pbkdf2_sha256.using(rounds=8000, salt_size=12).hash(password)
        return user

    def verify_password(self, password):
        return pbkdf2_sha256.verify(password, self.password_hash)

