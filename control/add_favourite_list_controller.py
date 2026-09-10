from typing import Tuple
from entity.favourite_list import FavouriteList


class add_favourite_list_controller:

    def addFavourite(self, accountId: int, activityId: int) -> Tuple[bool, str]:
        return FavouriteList.addFavourite(accountId, activityId)
