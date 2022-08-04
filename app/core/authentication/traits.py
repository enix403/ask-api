from app.core.authentication.roles import AuthRoles
from typing import Optional
from app.models.auth import AppUser
from authzx.traits import AgentTraitCollection

class TR:
    Everyone = 'sys.Everyone'
    Authenticated = 'sys.authncd'

    @staticmethod
    def BelongsToCollege(college_id):
        return f'app.ClgID({college_id})'

    @staticmethod
    def AuthRole(role):
        return f'app.ARole({role})'

    @staticmethod
    def StaffRole(role):
        return f'app.SRole({role})'

class SimpleTraitCollection(AgentTraitCollection):
    def get_effective_traits(self, user: Optional[AppUser]):
        if user is None:
            return [TR.Everyone]

        eff_traits = [
            TR.Everyone,
            TR.Authenticated,
            TR.AuthRole(user.auth_role)
        ]

        if user.auth_role == AuthRoles.Staff:
            eff_traits += [TR.StaffRole(user.staff_role), TR.BelongsToCollege(user.college_id)]

        return eff_traits


