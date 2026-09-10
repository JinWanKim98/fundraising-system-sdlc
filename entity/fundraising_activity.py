from dataclasses import dataclass
from typing import List, Optional, Tuple
from db import get_connection
from datetime import datetime
import sqlite3

@dataclass
class FundraisingActivity:
    """
    Entity class representing a fundraising activity.
    """
    activityId: Optional[int]
    accountId: int
    categoryId: int
    activityName: str
    activityDescription: str
    fundingGoal: float
    fundingCurrent: float
    activityStatus: str
    startDate: str
    endDate: str
    viewCount: int = 0
    favouriteCount: int = 0
    categoryName: Optional[str] = None
    fundraiserName: Optional[str] = None
    phoneNumber: Optional[str] = None    

    @classmethod
    def fromRow(cls, row) -> "FundraisingActivity":
        """
        Create a FundraisingActivity instance from a database row
        """
        row_keys = row.keys()
        return cls(
            activityId=row["activity_id"],
            accountId=row["account_id"],
            categoryId=row["category_id"],
            activityName=row["activity_name"],
            activityDescription=row["activity_desc"],
            fundingCurrent=row["funding_current"],
            fundingGoal=row["funding_goal"],
            startDate=row["start_date"],
            endDate=row["end_date"],
            activityStatus=row["activity_status"],
            viewCount=row["view_count"] if "view_count" in row_keys else 0,
            favouriteCount=row["favourite_count"] if "favourite_count" in row_keys else 0,
            categoryName=row["category_name"] if "category_name" in row_keys else None,
            fundraiserName=row["fundraiser_name"] if "fundraiser_name" in row_keys else None,
            phoneNumber=row["fundraiser_phone"] if "fundraiser_phone" in row_keys else None,
        )

    @classmethod
    def createActivity(
        cls,
        accountId: int,
        categoryId: int,
        activityName: str,
        activityDescription: str,
        fundingGoal: float,
        startDate: str,
        endDate: str
    ) -> Tuple[bool, str]:
        """
        Create and store a fundraising activity into database
        Returns:
            (success(Boolean), message)
        """

        activityName = activityName.strip()
        activityDescription = activityDescription.strip()
        startDate = startDate.strip()
        endDate = endDate.strip()

        connection = get_connection()

        try:
            connection.execute(
                """
                INSERT INTO fundraising_activity
                (account_id, category_id, activity_name, activity_desc,
                 funding_goal, funding_current, activity_status,
                 start_date, end_date)
                VALUES (?, ?, ?, ?, ?, 0, 'ongoing', ?, ?)
                """,
                (
                    accountId,
                    categoryId,
                    activityName,
                    activityDescription,
                    fundingGoal,
                    startDate,
                    endDate
                )
            )

            connection.commit()
            return True, f"Activity '{activityName}' created successfully."

        except sqlite3.IntegrityError:
            return False, "Invalid account ID or category ID."

        except sqlite3.Error as e:
            return False, f"Database error: {str(e)}"

        finally:
            connection.close()

    @classmethod
    def getAllActivities(cls) -> List["FundraisingActivity"]:
        """
        Return all fundraising activities
        """
        connection = get_connection()
        cursor = connection.execute(
    """
    SELECT 
        fra.*,

        (
            SELECT COUNT(*)
            FROM favourite_list fl
            WHERE fl.activity_id = fra.activity_id
        ) AS favourite_count,

        (
            SELECT COUNT(*)
            FROM activity_view av
            WHERE av.activity_id = fra.activity_id
        ) AS view_count,

        c.category_name,
        a.full_name AS fundraiser_name,
        a.contact_num AS fundraiser_phone

        FROM fundraising_activity fra
        JOIN user_account a 
            ON fra.account_id = a.account_id
        JOIN category c 
            ON fra.category_id = c.category_id

        ORDER BY fra.activity_id
        """
    )
        rows = cursor.fetchall()
        connection.close()

        return [cls.fromRow(row) for row in rows]

    @classmethod
    def getActivitiesByAccountId(cls, accountId: int) -> List["FundraisingActivity"]:
        """
        Return fundraising activities owned by one fundraiser account.
        """
        connection = get_connection()
        cursor = connection.execute(
            """
            SELECT
                fra.*,
                (
                    SELECT COUNT(*)
                    FROM favourite_list fl
                    WHERE fl.activity_id = fra.activity_id
                ) AS favourite_count,
                (
                    SELECT COUNT(*)
                    FROM activity_view av
                    WHERE av.activity_id = fra.activity_id
                ) AS view_count,
                c.category_name,
                a.full_name AS fundraiser_name,
                a.contact_num AS fundraiser_phone
            FROM fundraising_activity fra
            JOIN user_account a
              ON fra.account_id = a.account_id
            JOIN category c
              ON fra.category_id = c.category_id
            WHERE fra.account_id = ?
            ORDER BY fra.activity_id
            """,
            (accountId,)
        )
        rows = cursor.fetchall()
        connection.close()

        return [cls.fromRow(row) for row in rows]

    @classmethod
    def getActivityById(cls, activityId: int) -> Optional["FundraisingActivity"]:
        """
        Return one fundraising activity by activity ID.
        """
        connection = get_connection()
        cursor = connection.execute(
            """
            SELECT * FROM fundraising_activity
            WHERE activity_id = ?
            """,
            (activityId,)
        )
        row = cursor.fetchone()
        connection.close()

        if not row:
            return None

        return cls.fromRow(row)

    @classmethod
    def searchActivities(cls, searchTerm: str) -> List["FundraisingActivity"]:
        """
        Search activities by name or description
        """
        connection = get_connection()
        keyword = f"%{searchTerm.strip()}%"

        cursor = connection.execute(
            """
            SELECT * FROM fundraising_activity
            WHERE LOWER(activity_name) LIKE LOWER(?)
               OR LOWER(activity_desc) LIKE LOWER(?)
            ORDER BY activity_id
            """,
            (keyword, keyword)
        )

        rows = cursor.fetchall()
        connection.close()

        return [cls.fromRow(row) for row in rows]

    @classmethod
    def searchActivitiesByAccountId(cls, accountId: int, searchTerm: str) -> List["FundraisingActivity"]:
        """
        Search fundraising activities owned by one fundraiser account.
        """
        connection = get_connection()
        keyword = f"%{searchTerm.strip()}%"

        cursor = connection.execute(
            """
            SELECT
                fra.*,
                (
                    SELECT COUNT(*)
                    FROM favourite_list fl
                    WHERE fl.activity_id = fra.activity_id
                ) AS favourite_count,
                (
                    SELECT COUNT(*)
                    FROM activity_view av
                    WHERE av.activity_id = fra.activity_id
                ) AS view_count,
                c.category_name,
                a.full_name AS fundraiser_name,
                a.contact_num AS fundraiser_phone
            FROM fundraising_activity fra
            JOIN user_account a
              ON fra.account_id = a.account_id
            JOIN category c
              ON fra.category_id = c.category_id
            WHERE fra.account_id = ?
              AND (
                  LOWER(fra.activity_name) LIKE LOWER(?)
                  OR LOWER(fra.activity_desc) LIKE LOWER(?)
              )
            ORDER BY fra.activity_id
            """,
            (accountId, keyword, keyword)
        )

        rows = cursor.fetchall()
        connection.close()

        return [cls.fromRow(row) for row in rows]

    @classmethod
    def updateActivity(
        cls,
        activityId: int,
        activityName: str,
        activityDescription: str,
        fundingGoal: float,
        activityStatus: str
    ) -> Tuple[bool, str]:
        """
        Update an existing fundraising activity
        """

        connection = get_connection()

        try:
            cursor = connection.execute(
                "SELECT 1 FROM fundraising_activity WHERE activity_id = ?",
                (activityId,)
            )

            if not cursor.fetchone():
                return False, "Activity ID does not exist."

            connection.execute(
                """
                UPDATE fundraising_activity
                SET activity_name = ?, activity_desc = ?, 
                    funding_goal = ?, activity_status = ?
                WHERE activity_id = ?
                """,
                (
                    activityName.strip(),
                    activityDescription.strip(),
                    fundingGoal,
                    activityStatus.strip().lower(),
                    activityId
                )
            )

            connection.commit()
            return True, "Activity updated successfully."

        except sqlite3.IntegrityError:
            return False, "Invalid update data."

        except sqlite3.Error as e:
            return False, f"Database error: {str(e)}"

        finally:
            connection.close()

    @classmethod
    def deleteActivity(cls, activityId: int) -> Tuple[bool, str]:
        """
        Delete an existing fundraising activity
        """

        connection = get_connection()

        try:
            cursor = connection.execute(
                "SELECT 1 FROM fundraising_activity WHERE activity_id = ?",
                (activityId,)
            )

            if not cursor.fetchone():
                return False, "Activity ID does not exist."

            connection.execute(
                "DELETE FROM fundraising_activity WHERE activity_id = ?",
                (activityId,)
            )

            connection.commit()
            return True, "Activity deleted successfully."

        except sqlite3.Error as e:
            return False, f"Database error: {str(e)}"

        finally:
            connection.close()
        

    @classmethod
    def searchCompletedActivities(cls, keyword: str = "", categoryId: str = "", dateFrom: str = "", dateTo: str = "", accountId: Optional[int] = None) -> List["FundraisingActivity"]:

        connection = get_connection()

        query = """
            SELECT
                fra.*,
                (
                    SELECT COUNT(*)
                    FROM favourite_list fl
                    WHERE fl.activity_id = fra.activity_id
                ) AS favourite_count,
                (
                    SELECT COUNT(*)
                    FROM activity_view av
                    WHERE av.activity_id = fra.activity_id
                ) AS view_count,
                c.category_name,
                ua.full_name AS fundraiser_name,
                ua.contact_num AS fundraiser_phone
            FROM fundraising_activity fra
            JOIN category c
              ON fra.category_id = c.category_id
            JOIN user_account ua
              ON fra.account_id = ua.account_id
            WHERE fra.activity_status = 'completed'
        """

        params = []

        if accountId is not None:
            query += """
                AND fra.account_id = ?
            """
            params.append(accountId)

        if keyword.strip():
            searchKeyword = f"%{keyword.strip()}%"
            query += """
                AND (
                    LOWER(fra.activity_name) LIKE LOWER(?)
                    OR LOWER(fra.activity_desc) LIKE LOWER(?)
                )
            """
            params.extend([searchKeyword, searchKeyword])

        if categoryId:
            query += """
                AND fra.category_id = ?
            """
            params.append(categoryId)

        if dateFrom:
            query += """
                AND fra.end_date >= ?
            """
            params.append(dateFrom)

        if dateTo:
            query += """
                AND fra.end_date <= ?
            """
            params.append(dateTo)

        query += """
            ORDER BY fra.end_date DESC
        """

        cursor = connection.execute(query, tuple(params))
        rows = cursor.fetchall()
        connection.close()

        return [cls.fromRow(row) for row in rows]
    
    @classmethod
    def viewCompletedActivities(cls, accountId: Optional[int] = None) -> List["FundraisingActivity"]:
        """
        View all completed activities without search filter
        """
        connection = get_connection()
        query = """
            SELECT
                fra.*,
                (
                    SELECT COUNT(*)
                    FROM favourite_list fl
                    WHERE fl.activity_id = fra.activity_id
                ) AS favourite_count,
                (
                    SELECT COUNT(*)
                    FROM activity_view av
                    WHERE av.activity_id = fra.activity_id
                ) AS view_count,
                c.category_name,
                ua.full_name AS fundraiser_name,
                ua.contact_num AS fundraiser_phone
            FROM fundraising_activity fra
            JOIN category c
              ON fra.category_id = c.category_id
            JOIN user_account ua
              ON fra.account_id = ua.account_id
            WHERE fra.activity_status = 'completed'
            """
        params = []

        if accountId is not None:
            query += """
                AND fra.account_id = ?
            """
            params.append(accountId)

        query += """
            ORDER BY fra.activity_id
        """

        cursor = connection.execute(query, tuple(params))

        rows = cursor.fetchall()
        connection.close()

        return [cls.fromRow(row) for row in rows]


    @classmethod
    def recordView(cls, accountId: int, activityId: int) -> None:
        connection = get_connection()

        cursor = connection.execute(
            "SELECT MAX(viewing_id) FROM activity_view"
        )

        maxId = cursor.fetchone()[0]

        if maxId is None:
            newId = 1
        else:
            newId = maxId + 1

        viewingDate = datetime.now().strftime("%Y-%m-%d")

        connection.execute(
            """
            INSERT INTO activity_view
            (viewing_id, account_id, activity_id, viewing_date)
            VALUES (?, ?, ?, ?)
            """,
            (newId, accountId, activityId, viewingDate)
        )

        connection.commit()
        connection.close()
