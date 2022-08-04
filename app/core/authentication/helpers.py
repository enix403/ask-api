from authzx.traits import TraitSpec
from authzx.actions import Allow
from authzx.helpers import AclContext

class ContextGenerator:
    def generate(self, data):
        """
        Construct an ACL Context object (any object having 'acl' attribute) from the given request
        """
        return None


class RequireTraitContext(ContextGenerator):
    def __init__(self, trait):
        self.trait = trait

    def generate(self, data):
        return AclContext([(Allow, TraitSpec(self.trait), 'access')])