from typing import Tuple
from entity.user_account import UserAccount

class update_user_account_controller:
    """
    Control class responsible for updating user accounts.
    """
    def updateUserAccount(self, accountId: int, fullName: str, userName: str, passWord: str, birthday: str,
                          address: str, contact_number: str,
                          profileId: int, accountStatus: str) -> Tuple[bool, str]:
        return UserAccount.updateAccount(accountId, fullName, userName, passWord, birthday, address, contact_number, profileId, accountStatus)