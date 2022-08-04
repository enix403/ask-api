from typing import Any
import copy


class AgentTraitCollection():
    def __init__(self, agent_handle):
        self.agent_handle = agent_handle
        self._trait_list = self.get_effective_traits(agent_handle)

    def get_effective_traits(self, agent_handle: Any):
        return []

    def has_trait(self, trait):
        return trait in self._trait_list


class TraitSpec:
    OPER_AND = 'AND'
    OPER_OR = 'OR'

    OPER_DEFAULT = OPER_AND

    def __init__(self, *data):
        if len(data) != 0:
            self.children = [*copy.deepcopy(data)]
        else:
            self.children = []
        self.connector = self.OPER_DEFAULT
        self.negated = False

    def __str__(self):
        template = '(NOT (%s: %s))' if self.negated else '(%s: %s)'
        return template % (self.connector, ', '.join(str(c) for c in self.children))

    def __repr__(self):
        return "<%s: %s>" % (self.__class__.__name__, self)

    def add(self, data):
        self.children.append(data)

    def __and__(self, other):
        node = type(self)()
        node.connector = self.OPER_AND
        node.add(self)
        node.add(other)
        return node

    def __or__(self, other):
        node = type(self)()
        node.connector = self.OPER_OR
        node.add(self)
        node.add(other)
        return node

    def __invert__(self):
        node = type(self)()
        node.connector = self.OPER_AND
        node.add(self)
        node.negated = True
        return node
