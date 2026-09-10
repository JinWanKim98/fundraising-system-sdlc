from typing import Tuple
from entity.fundraising_activity import FundraisingActivity


class create_fundraising_activity_controller:
    """
    Control class responsible for creating fundraising activity.
    """

    def createActivity(self, account_id: int, category_id: int, name: str, desc: str, goal: float, start_date: str, end_date: str) -> Tuple[bool, str]:
        """
        Returns:
            (success(Boolean), message)
        """
        return FundraisingActivity.createActivity(account_id, category_id, name, desc, goal, start_date, end_date
        )
