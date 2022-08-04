from typing import Any, ClassVar, Optional, Type
from functools import wraps

from auth_core import (
    AuthorizationPolicy,
    AuthzGate,
    AgentTraitCollection,
    AclAuthorizationPolicy
)

from app.exceptions import ApiException, ApiExceptionCollection
from app.communication import ApiRequest
from app.models.auth import AppUser
from app.utils import to_int

from .keystore import KeyStore

class ContextGenerator:
    def generate(self, request: Optional[ApiRequest] = None):
        """
        Construct an ACL Context object (any object having 'acl' attribute) from the given request
        """
        return None

class TR:
    Everyone = 'sys.Everyone'
    Authenticated = 'sys.authncd'


class SimpleTraitCollection(AgentTraitCollection):
    def get_effective_traits(self, user: Optional[AppUser]):
        if user is None:
            return [TR.Everyone]

        eff_traits = [
            TR.Everyone,
            TR.Authenticated
        ]

        return eff_traits


class ApiPermissionGate:
    authz_policy = AclAuthorizationPolicy()
    next_exception: Exception = ApiExceptionCollection.Forbidden.copy_with(msg="Permission Denied")

    invalid_key_exp = ApiExceptionCollection.Forbidden.copy_with(msg="Permission Denied: Invalid Key")
    user_not_found_exp = ApiExceptionCollection.Forbidden.copy_with(msg="Permission Denied: User not found")

    # make sure it does not contain a whitespace
    _TOKEN_BEARER_PREFIX = 'API-Key'.strip()

    def __init__(self, request):
        self.user = self._load_user(request)
        self.gate = AuthzGate(SimpleTraitCollection(self.user), self.authz_policy)

    def inner(self):
        return self.gate

    def set_next_exception(self, exp: Exception):
        self.next_exception = exp

    @classmethod
    def get_token(cls, header: str):
        bearer_prefix, _, token = header.partition(' ')
        if bearer_prefix != cls._TOKEN_BEARER_PREFIX:
            return ''

        return token

    def _load_user(self, request) -> Optional[AppUser]:
        """ Load and return the user object from database or return None if not authenticated""" 
        api_key = self.get_token(request.META.get('HTTP_AUTHORIZATION', ''))

        # If no token is provided, show the regular 'permission denied' (default) error message
        if not api_key:
            return None

        try:
            hashed = KeyStore.hash_user(api_key)
            return AppUser.objects.filter(current_api_key=hashed).get()              
        except KeyStore.InvalidKeyError:
            self.set_next_exception(self.invalid_key_exp)
        except AppUser.DoesNotExist:
            self.set_next_exception(self.user_not_found_exp)

        return None


    def require(self, perm, context):
        if not self.gate.allowed(perm, context):
            raise self.next_exception

    # def require_one(self, perms, context):
    #     if not self.gate.allowed_one(perms, context):
    #         raise self.next_exception

    # def require_all(self, perms, context):
    #     if not self.gate.allowed_all(perms, context):
    #         raise self.next_exception



def require(perm: str, context_gen: ContextGenerator):
    def wrapper(func):
        @wraps(func)
        def _f(request, *args, **kwargs):
            ApiPermissionGate(request).require(perm, context_gen.generate(request))
            return func(request, *args, **kwargs)

        return _f

    return wrapper

