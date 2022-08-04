from collections import namedtuple

from auth_core.traits import TraitSpec
from auth_core.policy import Allow

AclContext = namedtuple('AclContext', ['acl'])

def make_ctx_require_all_traits(*traits):
    count = len(traits)
    assert count > 0, 'No traits given'

    if count == 1:
        return AclContext([(Allow, traits[0], {'access'})])

    spec = TraitSpec(traits[0])
    for t in traits[1:]:
        spec = spec & TraitSpec(t)

    return AclContext([(Allow, spec, {'access'})])


def make_ctx_require_any_trait(*traits):
    count = len(traits)
    assert count > 0, 'No traits given'

    if count == 1:
        return AclContext([(Allow, traits[0], {'access'})])

    spec = TraitSpec(traits[0])
    for t in traits[1:]:
        spec = spec | TraitSpec(t)

    return AclContext([(Allow, spec, {'access'})])