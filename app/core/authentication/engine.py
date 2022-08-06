from typing import Any, Optional
from functools import wraps

    # AuthzGate,
from auth_core import (
    AgentTraitCollection,
    AclAuthorizationPolicy
)

from app.exceptions import ApiException, ApiExceptionCollection
from app.communication import ApiRequest
from app.models.auth import AppUser

from .keystore import KeyStore

class ContextGenerator:
    def generate(self, request: Optional[ApiRequest] = None):
        """
        Construct an ACL Context object (any object having 'acl' attribute) from the given request
        """
        return None

class FixedContextGenerator(ContextGenerator):
    __slots__ = ('ctx',)
    def __init__(self, ctx: Any):
        self.ctx = ctx

    def generate(self, request: Optional[ApiRequest] = None):
        return self.ctx

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
    policy = AclAuthorizationPolicy()
    next_exception: Exception = ApiExceptionCollection.Forbidden.copy_with(msg="Permission Denied")

    invalid_key_exp = ApiExceptionCollection.Forbidden.copy_with(msg="Permission Denied: Invalid Key")
    user_not_found_exp = ApiExceptionCollection.Forbidden.copy_with(msg="Permission Denied: User not found")
    user_not_active_exp = ApiExceptionCollection.Forbidden.copy_with(msg="Permission Denied: User not active")

    # make sure it does not contain a whitespace
    _TOKEN_BEARER_PREFIX = 'Bearer'.strip()

    def __init__(self, request):
        self.user = self._load_user(request)
        self._traits = SimpleTraitCollection(self.user) 

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

        if not KeyStore.validate_format(api_key):
            self.set_next_exception(self.invalid_key_exp)
        else:
            user = AppUser.objects.filter(current_api_key=api_key).first()
            if user is None or user.is_deleted == 1:
                self.set_next_exception(self.user_not_found_exp)
            elif user.is_active == 0:
                self.set_next_exception(self.user_not_active_exp)
            else:
                return user

        return None

    def force_deny_request(self):
        raise self.next_exception

    def require(self, perm, context):
        self.policy.permits(perm, context, self._traits) or self.force_deny_request()


def require(perm: str, context_gen: ContextGenerator):
    def wrapper(func):
        @wraps(func)
        def _f(request, *args, **kwargs):
            gate = ApiPermissionGate(request)
            gate.require(perm, context_gen.generate(request))
            request.user = gate.user
            return func(request, *args, **kwargs)

        return _f

    return wrapper

