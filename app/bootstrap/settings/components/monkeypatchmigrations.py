# Django doesn't like when its models inherit from anything other than models.Model
# However making models inherit from typings.Generic is necessary to provide accurate code
# completions from python language server. This file removes typing.Generic from list of class bases
# of the model classes so that Django doesn't explode 

# See https://github.com/typeddjango/django-stubs/issues/299

from django.db.migrations.state import ModelState
from typing import Generic

_original = ModelState.render

def _new(self, apps):
    self.bases = tuple(base for base in self.bases if not issubclass(base, Generic))  # type: ignore
    return _original(self, apps)

ModelState.render = _new  # type: ignore