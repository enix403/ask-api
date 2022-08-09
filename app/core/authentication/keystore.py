import secrets
from collections import namedtuple

from app.utils.passlib_hash import pbkdf2_sha256


# Helper class for managing API keys
class KeyStore:

    # class InvalidKeyError(Exception):
        # pass

    API_KEY_APP_PREFIX = 'kp.'
    API_KEY_APP_PREFIX_LENGTH = len(API_KEY_APP_PREFIX)

    GeneratedAPIKey = namedtuple('GeneratedAPIKey', ['prefix', 'digest'])

    @classmethod
    def generate_fresh(cls) -> GeneratedAPIKey:
        """ Generate a fresh key """
        return cls.GeneratedAPIKey(
            prefix=secrets.token_urlsafe(6),
            digest=secrets.token_urlsafe(32)
        )

    @classmethod
    def serialize_user(cls, key: GeneratedAPIKey) -> str:
        """ Serialzes the key, which can then be sent to the user"""

        # format := {2-byte app id}.{6-byte prefix}.{32-byte api key}
        #
        # In the future we might decide to store in db the hash of the key instead of *the key* itself. In that
        # case we can use this `prefix` for manual key identification (e.g if a client has multiple keys and need to pick
        # the correct one, maybe based on the key's scope). The prefix will be stored unhased while the rest of the key is hashed
        return ''.join([
            cls.API_KEY_APP_PREFIX,
            key.prefix,
            '.',
            key.digest,
        ]);

    @classmethod
    def validate_format(cls, user_key: str) -> bool:
        # Enough for now
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

