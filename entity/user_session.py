from dataclasses import dataclass
from typing import List, Optional, Tuple
from db import get_connection
import sqlite3


@dataclass
class UserSession:
    """
    Entity class representing a user login session.
    """
    sessionId: Optional[int]
    accountId: int
    loginAt: str
    logoutAt: Optional[str]
    sessionStatus: str

    @classmethod
    def fromRow(cls, row) -> "UserSession":
        """
        Create a UserSession instance from a database row.
        """
        logout_at = row["logout_at"] if row["logout_at"] else None
        return cls(
            sessionId=row["session_id"],
            accountId=row["account_id"],
            loginAt=row["login_at"],
            logoutAt=logout_at,
            sessionStatus=row["session_status"]
        )

    @classmethod
    def createSession(cls, accountId: int) -> Tuple[bool, str, Optional["UserSession"]]:
        """
        Create a new active login session for an account.
        """
        connection = get_connection()

        try:
            cursor = connection.execute(
                """
                INSERT INTO user_session (account_id, login_at, logout_at, session_status)
                VALUES (?, CURRENT_TIMESTAMP, NULL, 'active')
                """,
                (accountId,)
            )
            connection.commit()

            row = connection.execute(
                """
                SELECT session_id, account_id, login_at, logout_at, session_status
                FROM user_session
                WHERE session_id = ?
                """,
                (cursor.lastrowid,)
            ).fetchone()

            return True, "Login session created successfully.", cls.fromRow(row)

        except sqlite3.IntegrityError:
            return False, "Invalid account ID.", None

        except sqlite3.Error as e:
            return False, f"Database error: {str(e)}", None

        finally:
            connection.close()

    @classmethod
    def findActiveSessionByAccountId(cls, accountId: int) -> Optional["UserSession"]:
        """
        Find the latest active session for the given account.
        """
        connection = get_connection()
        cursor = connection.execute(
            """
            SELECT session_id, account_id, login_at, logout_at, session_status
            FROM user_session
            WHERE account_id = ?
              AND session_status = 'active'
            ORDER BY session_id DESC
            LIMIT 1
            """,
            (accountId,)
        )
        row = cursor.fetchone()
        connection.close()

        if not row:
            return None

        return cls.fromRow(row)

    @classmethod
    def logoutSession(cls, sessionId: int) -> Tuple[bool, str]:
        """
        Mark an active session as logged out.
        """
        connection = get_connection()

        try:
            cursor = connection.execute(
                """
                SELECT 1
                FROM user_session
                WHERE session_id = ?
                  AND session_status = 'active'
                """,
                (sessionId,)
            )
            row = cursor.fetchone()

            if not row:
                return False, "Active session not found."

            connection.execute(
                """
                UPDATE user_session
                SET logout_at = CURRENT_TIMESTAMP,
                    session_status = 'logged_out'
                WHERE session_id = ?
                """,
                (sessionId,)
            )
            connection.commit()
            return True, "Logged out successfully."

        except sqlite3.Error as e:
            return False, f"Database error: {str(e)}"

        finally:
            connection.close()

    @classmethod
    def getSessionsByAccountId(cls, accountId: int) -> List["UserSession"]:
        """
        Return session history for the given account.
        """
        connection = get_connection()
        cursor = connection.execute(
            """
            SELECT session_id, account_id, login_at, logout_at, session_status
            FROM user_session
            WHERE account_id = ?
            ORDER BY session_id DESC
            """,
            (accountId,)
        )
        rows = cursor.fetchall()
        connection.close()

        return [cls.fromRow(row) for row in rows]
