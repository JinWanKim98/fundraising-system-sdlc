from typing import Tuple
from entity.fundraising_activity import FundraisingActivity


class update_fundraising_activity_controller:
    """
    Control class responsible for updating fundraising activity.
    """
    def updateActivity(self, activity_id: int, name: str, desc: str, goal: float, status: str) -> Tuple[bool, str]:
        return FundraisingActivity.updateActivity(activity_id, name, desc, goal, status)
