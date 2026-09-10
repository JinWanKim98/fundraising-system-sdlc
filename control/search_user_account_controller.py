from typing import List
from entity.user_account import UserAccount

class search_user_account_controller:
    """
    Control class responsible for searching user accounts.
    """
    def searchAccounts(self, searchTerm: str) -> List[UserAccount]:
        return UserAccount.searchAccounts(searchTerm)