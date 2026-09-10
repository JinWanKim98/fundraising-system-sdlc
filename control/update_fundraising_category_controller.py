from typing import Tuple
from entity.fundraising_category import FundraisingCategory


class update_fundraising_category_controller:
    """
    Control class responsible for updating fundraising categories.
    """
    def updateFundraisingCategory(self, categoryId: int, categoryName: str) -> Tuple[bool, str]:
        return FundraisingCategory.updateCategory(categoryId, categoryName)