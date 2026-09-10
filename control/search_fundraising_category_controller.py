from typing import Optional
from entity.fundraising_category import FundraisingCategory

class search_fundraising_category_controller:
    """
    Control class responsible for searching fundraising categories.
    """
    def searchCategories(self, searchTerm: str) -> Optional["FundraisingCategory"]:
        return FundraisingCategory.searchCategories(searchTerm)