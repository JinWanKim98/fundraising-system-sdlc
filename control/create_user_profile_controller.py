from typing import Tuple
from entity.user_profile import UserProfile


class create_user_profile_controller:
    """
    Control class responsible for creating user profiles.
    """

    def createUserProfile(self, profileName: str, profileDescription: str) -> Tuple[bool, str]:
        """
        Returns:
            (success(Boolean), message)
        """
        return UserProfile.createProfile(profileName, profileDescription)