from dataclasses import dataclass
from typing import List, Optional, Tuple
from db import get_connection
from datetime import date
import sqlite3

@dataclass
class UserAccount:
    """
    Entity class representing a user account that contains
    individual information
    """
    accountId: Optional[int]
    fullName: str
    userName: str
    passWord: str
    birthday: Optional[str]
    address: Optional[str]
    contact_number: str
    profileId: int
    accountStatus: str
    accountCreatedDate: Optional[str]

    @classmethod
    def fromRow(cls, row) -> "UserAccount":
        """
        create a UserAccount instance from a database row
        """
        return cls(
            accountId = row["account_id"],
            fullName = row["full_name"],
            userName = row["username"],
            passWord = row["password"],
            birthday = row["DOB"],
            address = row["address"],
            contact_number = row["contact_num"],
            profileId = row["profile_id"],
            accountStatus = row["account_status"],
            accountCreatedDate = row["account_created_date"]
            )

    @classmethod
    def usernameExists(cls, userName: str) -> bool:
        """
        Checks if an account with the same username exists
        """
        connection = get_connection()
        cursor = connection.execute(
            """
            SELECT 1
            FROM user_account
            WHERE LOWER(username) = LOWER(?)
            """,
            (userName.strip(),)
        )
        row = cursor.fetchone()
        connection.close()
        return row is not None

    @classmethod
    def createAccount(cls, fullName: str, userName: str, passWord: str, birthday: str,
                      address: str, contact_number: str, profileId: int, accountStatus: str = "ACTIVE"):
        """
        Create and store a User Account into database
        """
        fullName = fullName.strip()
        userName = userName.strip()
        passWord = passWord.strip()
        birthday = birthday.strip()
        address = address.strip()
        contact_number = contact_number.strip()
        accountStatus = accountStatus.strip().upper()


        if not fullName:
            raise ValueError("Full name is required.")

        if not userName:
            raise ValueError("Username is required.")

        if not passWord:
            raise ValueError("Password is required.")

        if not contact_number:
            raise ValueError("Contact number is required.")

        valid_statuses = ["ACTIVE", "SUSPENDED", "EXPIRED"]
        if accountStatus not in valid_statuses:
            raise ValueError("Invalid account status.")

        if cls.usernameExists(userName):
            raise ValueError(f"User {userName} already exists.")
        else:
            connection = get_connection()
            cursor = connection.execute(
                """
                INSERT INTO user_account (full_name, username, password, 
                                          DOB, address, contact_num, profile_id, account_status, account_created_date)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (fullName, userName, passWord,
                 birthday, address, contact_number, profileId, accountStatus, date.today().isoformat())

            )
            connection.commit()
            new_account = cls(
                accountId = cursor.lastrowid,
                fullName = fullName,
                userName = userName,
                passWord = passWord,
                birthday = birthday,
                address = address,
                contact_number = contact_number,
                profileId = profileId,
                accountStatus = accountStatus,
                accountCreatedDate = date.today().isoformat()
            )
            connection.close()
            return new_account

    @classmethod
    def getAllAccounts(cls) -> List["UserAccount"]:
        """
        Return all user accounts from the database
        """
        connection = get_connection()
        cursor = connection.execute(
            """
            SELECT account_id, full_name, username, password, DOB, 
            address, contact_num, profile_id, account_status, account_created_date
            FROM user_account
            ORDER BY account_id
            """
        )
        rows = cursor.fetchall()
        connection.close()

        return [cls.fromRow(row) for row in rows]

    @classmethod
    def searchAccounts(cls, searchTerm: str) -> List["UserAccount"]:
        """
        Search user accounts by name, username, contact number, or status
        """
        connection = get_connection()
        keyword = f"%{searchTerm.strip()}%"

        cursor = connection.execute(
            """
            SELECT account_id, full_name, username, password, DOB, 
            address, contact_num, profile_id, account_status, account_created_date
            FROM user_account
            WHERE LOWER(full_name) LIKE LOWER(?)
                OR LOWER(username) LIKE LOWER(?)
                OR LOWER(contact_num) LIKE LOWER(?)
                OR LOWER(account_status) LIKE LOWER(?)
            ORDER BY account_id
            """,
            (keyword, keyword, keyword, keyword)
            )
        rows = cursor.fetchall()
        connection.close()
        return [cls.fromRow(row) for row in rows]

    @classmethod
    def updateAccount(cls, accountId: int, fullName: str, userName: str, passWord: str, birthday: str, address: str,
                      contact_number: str, profileId: int, accountStatus: str) -> Tuple[bool, str]:
        """
        Update existing user account in database
        """
        fullName = fullName.strip()
        userName = userName.strip()
        passWord = passWord.strip()
        birthday = birthday.strip()
        address = address.strip()
        contact_number = contact_number.strip()
        accountStatus = accountStatus.strip().upper()

        if not fullName:
            return False, "Full name is required."
        if not userName:
            return False, "Username is required."
        if not passWord:
            return False, "Password is required."
        if not contact_number:
            return False, "Contact number is required."

        valid_statuses = ["ACTIVE", "SUSPENDED", "EXPIRED"]
        if accountStatus not in valid_statuses:
            return False, "Invalid account status."
        connection = get_connection()

        try:
            cursor = connection.execute(
                """
                SELECT 1
                FROM user_account
                WHERE account_id = ?
                """,
                (accountId,)
            )

            row = cursor.fetchone()

            if not row:
                return False, "Account id does not exist."
            cursor = connection.execute(
                """
                SELECT 1
                FROM user_account
                WHERE LOWER(username) = LOWER(?)
                    AND account_id != ?
                """,
                (userName, accountId)
            )

            duplicate_row = cursor.fetchone()
            if duplicate_row:
                return False, "Username already exists."
            connection.execute(
                """
                UPDATE user_account
                SET full_name = ?, username = ?, password = ?, DOB = ?, address = ?, 
                    contact_num = ?, profile_id = ?, account_status = ?
                WHERE account_id = ?
                """,
                (
                    fullName, userName, passWord, birthday, address, contact_number, profileId, accountStatus, accountId
                )
            )
            connection.commit()
            return True, "Account updated successfully."
        except sqlite3.IntegrityError:
            return False, "Invalid profile ID/Username already exists."
        except sqlite3.Error as e:
            return False, f"Database error: {str(e)}"
        finally:
            connection.close()

    @classmethod
    def suspendAccount(cls, accountId: int) -> Tuple[bool, str]:
        """
        Suspend an existing user account
        """
        connection = get_connection()
        try:
            cursor = connection.execute(
                """
                SELECT 1
                FROM user_account
                WHERE account_id = ?
                """,
                (accountId,)
            )
            row = cursor.fetchone()

            if not row:
                return False, "Account id does not exist."

            connection.execute(
                """
                UPDATE user_account
                SET account_status = 'SUSPENDED'
                WHERE account_id = ?
                """,
                (accountId,)
            )
            connection.commit()
            return True, "Account suspended successfully."
        except sqlite3.Error as e:
            return False, f"Database error: {str(e)}"
        finally:
            connection.close()

    @classmethod
    def authenticateUser(cls, userName: str, passWord: str) -> "UserAccount":
        """
        Authenticate an existing user account
        """
        userName = userName.strip()
        passWord = passWord.strip()

        if not userName:
            raise ValueError("Username is required.")
        if not passWord:
            raise ValueError("Password is required.")

        connection = get_connection()
        cursor = connection.execute(
            """
            SELECT account_id, full_name, username, password, DOB,
                   address, contact_num, profile_id, account_status, account_created_date
            FROM user_account
            WHERE LOWER(username) = LOWER(?)
                AND password = ?
            """,
            (userName, passWord)
        )
        row = cursor.fetchone()
        connection.close()

        if not row:
            raise ValueError("Invalid username or password.")

        account = cls.fromRow(row)

        if account.accountStatus != "ACTIVE":
            raise ValueError(f"Account is {account.accountStatus.lower()}.")
        return account