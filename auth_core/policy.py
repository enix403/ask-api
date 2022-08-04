from auth_core.traits import AgentTraitCollection, TraitSpec
from typing import Container, Iterable, Any, cast

#######################################
############### ACTIONS ###############
#######################################

Allow   = 1
Deny    = 0


########################################
############### POLICIES ###############
########################################


class AuthorizationPolicy(object):
    def permits(self, permission, resource_context: Any, traits: AgentTraitCollection) -> bool:
        """
            Returns `True` if `permission` is granted according to the given traits and context,
            `False` otherwise
        """
        raise NotImplemented();

    def all_permissions(self, resource_context: Any, traits: AgentTraitCollection) -> Iterable:
        """
            Returns a list of all permissions granted to the user according to the given traits and context
        """
        raise NotImplemented();

def _resolve_control(root_node: TraitSpec, traits: AgentTraitCollection):
    resolved = root_node.connector == TraitSpec.OPER_AND
    for child in root_node.children:
        if isinstance(child, TraitSpec):
            resolve_child = _resolve_control(child, traits)
        else:
            resolve_child = traits.has_trait(child)

        if root_node.connector == TraitSpec.OPER_AND:
            if not resolve_child:
                resolved = False
                break

        else:
            if resolve_child:
                resolved = True
                break

    if root_node.negated:
        resolved = not resolved

    return resolved


class AclAuthorizationPolicy(AuthorizationPolicy):
    def permits(self, permission, resource_context: Any, agent_traits: AgentTraitCollection) -> bool:

        try:
            acl = resource_context.acl
        except AttributeError:
            return False

        allowed = False

        for (action, trait, granted_perms) in acl:
            assert (action is Allow or action is Deny), f"Invalid action: {action}"
            granted_perms = cast(Container, granted_perms)
            if not (permission in granted_perms):
                continue

            if isinstance(trait, TraitSpec):
                passed = _resolve_control(trait, agent_traits)
            else:
                passed = agent_traits.has_trait(trait)

            if passed:
                allowed = action is Allow

        return allowed


    def all_permissions(self, resource_context: Any, agent_traits: AgentTraitCollection) -> Iterable:
        try:
            acl = resource_context.acl
        except AttributeError:
            return []

        all_perms = set()

        for (action, trait, perms) in acl:
            assert (action is Allow or action is Deny), f"Invalid action: {action}"
            if isinstance(trait, TraitSpec):
                passed = _resolve_control(trait, agent_traits)
            else:
                passed = agent_traits.has_trait(trait)

            if passed:
                if action == Allow:
                    all_perms.update(perms)
                else:
                    all_perms.difference_update(perms)
            
        return all_perms

