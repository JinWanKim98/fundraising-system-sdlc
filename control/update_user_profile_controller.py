from typing import Tuple
from entity.user_profile import UserProfile


class update_user_profile_controller:
    """
    Control class responsible for updating user profiles.
    """
    def updateUserProfile(self, profileId: int, profileName: str, profileDescription: str) -> Tuple[bool, str]:
        return UserProfile.updateProfile(profileId, profileName, profileDescription)