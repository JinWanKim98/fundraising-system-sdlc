from typing import Tuple
from entity.user_profile import UserProfile


class delete_user_profile_controller:
    """
    Control class responsible for deleting user profiles.
    """
    def deleteUserProfile(self, profileId: int) -> Tuple[bool, str]:
        return UserProfile.deleteProfile(profileId)