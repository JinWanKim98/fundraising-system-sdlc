from typing import Tuple
from entity.user_account import UserAccount

class create_user_account_controller:
    """
    control class responsible for creating user account
    """
    def createUserAccount(self, fullName: str, userName: str, passWord: str, birthday: str,
                          address: str, contact_number: str, profileId: int,
                          accountStatus: str = "ACTIVE") -> Tuple[bool, str]:
        """
        Returns:
            (success(Boolean), message)
        """
        try:
            UserAccount.createAccount(fullName, userName, passWord, birthday,
                                      address, contact_number, profileId, accountStatus)
            return True, "Account created successfully."
        except ValueError as e:
            return False, str(e)