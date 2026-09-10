from typing import Tuple, Optional
from entity.fundraising_activity import FundraisingActivity


class search_completed_activity_controller:
    """
    Control class responsible for searching completed fundraising activities.
    """
    def searchCompletedActivities(self, searchTerm: str, categoryId: str = "", dateFrom: str = "", dateTo: str = "") -> Optional["FundraisingActivity"]:
        return FundraisingActivity.searchCompletedActivities(searchTerm, categoryId, dateFrom, dateTo)

    def searchCompletedActivitiesByAccountId(self, accountId: int, searchTerm: str, categoryId: str = "", dateFrom: str = "", dateTo: str = "") -> Optional["FundraisingActivity"]:
        return FundraisingActivity.searchCompletedActivities(searchTerm, categoryId, dateFrom, dateTo, accountId)
