from typing import Optional, Tuple
from entity.user_account import UserAccount
from entity.user_session import UserSession

"""
Controller receive username and password from boundary, authenticates
then creates a login session and return a result to the route
"""

class login_controller:
    """
    control class responsible for login:
    """
    def loginUser(self, userName: str, passWord: str) -> Tuple[bool, str, Optional[UserAccount], Optional[UserSession]]:
        try:
            account = UserAccount.authenticateUser(userName, passWord)
            success, message, session = UserSession.createSession(account.accountId)

            if not success:
                return False, message, None, None
            return True, "Login Successful", account, session

        except ValueError as e:
            return False, str(e), None, None