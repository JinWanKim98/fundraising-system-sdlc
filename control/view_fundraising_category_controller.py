from typing import List, Optional
from entity.fundraising_category import FundraisingCategory

class view_fundraising_category_controller:
    """
    Control class responsible for retrieving fundraising category details.
    """

    def viewFundraisingCategory(self) -> List["FundraisingCategory"]:
        """
        Retrieve all fundraising category object.
        """
        return FundraisingCategory.getAllCategories()

    def viewCategoryById(self, category_id: int) -> Optional["FundraisingCategory"]:
        """
        Retrieve one fundraising category object by category ID.
        """
        return FundraisingCategory.getCategoryById(category_id)
