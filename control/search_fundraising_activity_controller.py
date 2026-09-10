from typing import Tuple, Optional
from entity.fundraising_activity import FundraisingActivity


class search_fundraising_activity_controller:
    """
    Control class responsible for searching fundraising activity.
    """
    def searchActivities(self, searchTerm: str) -> Optional["FundraisingActivity"]:
        return FundraisingActivity.searchActivities(searchTerm)

    def searchActivitiesByAccountId(self, accountId: int, searchTerm: str) -> Optional["FundraisingActivity"]:
        return FundraisingActivity.searchActivitiesByAccountId(accountId, searchTerm)
