from entity.favourite_list import FavouriteList


class search_favourite_list_controller:

    def searchFavourites(self, accountId: int, searchTerm: str):
        return FavouriteList.searchFavouritesByAccountId(accountId, searchTerm)
