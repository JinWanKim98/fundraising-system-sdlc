from entity.fundraising_activity import FundraisingActivity


class fundraising_activity_view_record_controller:
    """
    Control class responsible for recording views of fundraising activities.
    """
    def recordActivityView(self, accountId: int, activityId: int) -> None:
        return FundraisingActivity.recordView(accountId, activityId)