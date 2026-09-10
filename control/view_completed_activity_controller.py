from typing import List
from entity.fundraising_activity import FundraisingActivity

class view_completed_activity_controller:
    """
    Control class responsible for retrieving fundraising activity details.
    """

    def viewCompletedActivities(self) -> List["FundraisingActivity"]:
        """
        Retrieve all Fundraising Activity object.
        """
        return FundraisingActivity.viewCompletedActivities()

    def viewCompletedActivitiesByAccountId(self, accountId: int) -> List["FundraisingActivity"]:
        """
        Retrieve completed fundraising activities owned by one account.
        """
        return FundraisingActivity.viewCompletedActivities(accountId)
