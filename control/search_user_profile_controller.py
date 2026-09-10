from typing import Tuple, Optional
from entity.user_profile import UserProfile


class search_user_profile_controller:
    """
    Control class responsible for searching user profiles.
    """
    def searchProfiles(self, searchTerm: str) -> Optional["UserProfile"]:
        return UserProfile.searchProfiles(searchTerm)
    