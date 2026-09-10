from typing import Tuple
from entity.user_account import UserAccount

class suspend_user_account_controller:
    """
    Control class responsible for suspend user accounts.
    """
    def suspendUserAccount(self, accountId: int) -> Tuple[bool, str]:
        return UserAccount.suspendAccount(accountId)