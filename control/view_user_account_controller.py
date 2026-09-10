from typing import List
from entity.user_account import UserAccount

class view_user_account_controller:
    """
    Control class responsible for retrieving user accounts.
    """
    def viewUserAccount(self) -> List["UserAccount"]:
        """
        Retrieve all user account objects.
        """
        return UserAccount.getAllAccounts()