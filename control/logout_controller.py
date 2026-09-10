from typing import Tuple
from entity.user_session import UserSession


"""
Receive sessionId then call logout session from UserSession
then returns success/failure
"""

class logout_controller:
    """
    Control class responsible for logging users out.
    """
    def logoutUser(self, sessionId: int) -> Tuple[bool, str]:
        return UserSession.logoutSession(sessionId)