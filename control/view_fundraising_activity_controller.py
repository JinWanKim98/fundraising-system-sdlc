from typing import List, Optional
from entity.fundraising_activity import FundraisingActivity

class view_fundraising_activity_controller:
    """
    Control class responsible for retrieving fundraising activity details.
    """

    def viewActivities(self) -> List["FundraisingActivity"]:
        """
        Retrieve all Fundraising Activity object.
        """
        return FundraisingActivity.getAllActivities()

    def viewActivitiesByAccountId(self, account_id: int) -> List["FundraisingActivity"]:
        """
        Retrieve fundraising activities owned by one account.
        """
        return FundraisingActivity.getActivitiesByAccountId(account_id)

    def viewActivityById(self, activity_id: int) -> Optional["FundraisingActivity"]:
        """
        Retrieve one Fundraising Activity object by activity ID.
        """
        return FundraisingActivity.getActivityById(activity_id)
