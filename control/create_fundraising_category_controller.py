from typing import Tuple
from entity.fundraising_category import FundraisingCategory

class create_fundraising_category_controller:
    """
    Control class responsible for creating fundraising categories.
    """

    def createFundraisingCategory(self, categoryName: str) -> Tuple[bool, str]:
        """
        Create a new fundraising category.
        Returns:
            (success(Boolean), message)
        """
        return FundraisingCategory.createCategory(categoryName)