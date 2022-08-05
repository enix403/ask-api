import secrets
from collections import namedtuple

from app.utils.passlib_hash import pbkdf2_sha256

class KeyStore:

    # class InvalidKeyError(Exception):
        # pass

    API_KEY_APP_PREFIX = 'kp.'
    API_KEY_APP_PREFIX_LENGTH = len(API_KEY_APP_PREFIX)

    GeneratedAPIKey = namedtuple('GeneratedAPIKey', ['prefix', 'digest'])

    @classmethod
    def generate_fresh(cls) -> GeneratedAPIKey:
        return cls.GeneratedAPIKey(
            prefix=secrets.token_urlsafe(6),
            digest=secrets.token_urlsafe(32)
        )

    @classmethod
    def serialize_user(cls, key: GeneratedAPIKey) -> str:
        # format = {2-byte app id}.{6-byte prefix}.{32-byte api key}
        return ''.join([
            cls.API_KEY_APP_PREFIX,
            key.prefix,
            '.',
            key.digest,
        ]);

    @classmethod
    def validate_format(cls, user_key: str) -> bool:
        # enough for now
        return user_key.startswith(cls.API_KEY_APP_PREFIX)


    # @classmethod
    # def _hash_impl(cls, serialzed) -> str:
    #     return pbkdf2_sha256.using(
    #         rounds=1000,
    #         salt_size=12
    #     ).hash(serialzed)

    # @classmethod
    # def hash_raw(cls, key: GeneratedAPIKey) -> str:
    #     return cls._hash_impl(cls.serialize_user(key))

    # @classmethod
    # def hash_user(cls, user_key: str) -> str:
    #     if not user_key.startswith(cls.API_KEY_APP_PREFIX):
    #         raise KeyStore.InvalidKeyError()

    #     return cls._hash_impl(user_key)

