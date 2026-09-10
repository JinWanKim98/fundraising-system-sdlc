from typing import Tuple
from entity.fundraising_category import FundraisingCategory

class delete_fundraising_category_controller:
    """
    Control class responsible for deleting fundraising categories.
    """
    def deleteFundraisingCategory(self, categoryId: int) -> Tuple[bool, str]:
        """
        Delete a fundraising category by its ID.
        Returns:
            (success(Boolean), message)
        """
        return FundraisingCategory.deleteCategory(categoryId)