from typing import Tuple
from entity.fundraising_activity import FundraisingActivity


class delete_fundraising_activity_controller:
    """
    Control class responsible for deleting fundraising activity.
    """
    def deleteActivity(self, activity_id: int) -> Tuple[bool, str]:
        return FundraisingActivity.deleteActivity(activity_id)
