from typing import Optional, Any


from auth_core.policy import (
    Allow,
    Deny,
    AuthorizationPolicy,
    AclAuthorizationPolicy
)

from auth_core.traits import (
    AgentTraitCollection,
    TraitSpec
)

from auth_core.helpers import (
    AclContext,

    make_ctx_require_all_traits,
    make_ctx_require_any_trait

)


class AuthzGate():
    def __init__(self, traits: AgentTraitCollection, policy: Optional[AuthorizationPolicy]=None):
        self._traits = traits
        
        if policy is None:
            self._policy = AclAuthorizationPolicy()
        else:
            self._policy = policy


    def get_policy(self) -> AuthorizationPolicy:
        return self._policy

    def get_traits(self):
        return self._traits

    def allowed(self, permission, context):
        return self._policy.permits(permission, context, self._traits)

    def allowed_all(self, permissions, context):
        for perm in permissions:
            if not self._policy.permits(perm, context, self._traits):
                return False

        return False

    def allowed_one(self, permissions, context):
        for perm in permissions:
            if not self._policy.permits(perm, context, self._traits):
                return True

        return False

    def all_permissions(self, context: Any):
        return self._policy.all_permissions(context, self._traits)
