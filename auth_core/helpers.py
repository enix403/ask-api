from collections import namedtuple

from auth_core.traits import TraitSpec
from auth_core.policy import Allow

class AclContext(object):
    __slots__ = ('acl')
    def __init__(self, *acl):
        self.acl = acl

    @classmethod
    def singular(cls, action, trait, granted_perms):
        # Just to avoid extra parenthesis while creating unit-length contexts
        return cls((action, trait, granted_perms))

def make_ctx_require_all_traits(*traits):
    count = len(traits)
    assert count > 0, 'No traits given'

    if count == 1:
        return AclContext.singular(Allow, traits[0], {'access'})

    spec = TraitSpec(traits[0])
    for t in traits[1:]:
        spec = spec & TraitSpec(t)

    return AclContext.singular(Allow, spec, {'access'})


def make_ctx_require_any_trait(*traits):
    count = len(traits)
    assert count > 0, 'No traits given'

    if count == 1:
        AclContext.singular(Allow, traits[0], {'access'})

    spec = TraitSpec(traits[0])
    for t in traits[1:]:
        spec = spec | TraitSpec(t)

    return AclContext.singular(Allow, spec, {'access'})