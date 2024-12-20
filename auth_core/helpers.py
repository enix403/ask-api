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

    @classmethod
    def trait_singular(cls, trait):
        return cls((Allow, trait, {'access'}))

    @classmethod
    def trait_all(cls, *traits):
        count = len(traits)
        assert count > 0, 'No traits given'

        if count == 1:
            return cls.trait_singular(traits[0])

        spec = TraitSpec(traits[0])
        for t in traits[1:]:
            spec = spec & TraitSpec(t)

        return cls.trait_singular(spec)

    @classmethod
    def trait_any(cls, *traits):
        count = len(traits)
        assert count > 0, 'No traits given'

        if count == 1:
            return cls.trait_singular(traits[0])

        spec = TraitSpec(traits[0])
        for t in traits[1:]:
            spec = spec | TraitSpec(t)

        return cls.trait_singular(spec)
