from dataclasses import dataclass
from typing import List, Tuple
from db import get_connection
import sqlite3


@dataclass
class FavouriteList:
    favouriteId: int
    accountId: int
    activityId: int
    activityName: str
    activityDescription: str
    activityStatus: str
    categoryId: int
    fundingCurrent: float
    fundingGoal: float
    startDate: str
    endDate: str
    viewCount: int = 0
    favouriteCount: int = 0
    categoryName: str = ""
    fundraiserName: str = ""
    phoneNumber: str = ""

    @classmethod
    def fromRow(cls, row):
        return cls(
            favouriteId=row["favourite_id"],
            accountId=row["account_id"],
            activityId=row["activity_id"],
            activityName=row["activity_name"],
            activityDescription=row["activity_desc"],
            activityStatus=row["activity_status"],
            categoryId=row["category_id"],
            fundingCurrent=row["funding_current"],
            fundingGoal=row["funding_goal"],
            startDate=row["start_date"],
            endDate=row["end_date"],
            viewCount=row["view_count"],
            favouriteCount=row["favourite_count"],
            categoryName=row["category_name"],
            fundraiserName=row["fundraiser_name"],
            phoneNumber=row["fundraiser_phone"]
        )

    # ADD
    @classmethod
    def addFavourite(cls, accountId: int, activityId: int) -> Tuple[bool, str]:
        connection = get_connection()

        try:
            connection.execute(
                """
                INSERT INTO favourite_list (account_id, activity_id)
                VALUES (?, ?)
                """,
                (accountId, activityId)
            )
            connection.commit()
            return True, "Activity added to favourites."

        except sqlite3.IntegrityError:
            return False, "Activity is already in favourites."

        except sqlite3.Error as e:
            return False, f"Database error: {str(e)}"

        finally:
            connection.close()

    # VIEW
    @classmethod
    def getFavouritesByAccountId(cls, accountId: int) -> List["FavouriteList"]:
        connection = get_connection()

        cursor = connection.execute(
            """
            SELECT f.*, a.activity_name, a.activity_desc,
                   a.activity_status, a.category_id,
                   a.funding_current, a.funding_goal,
                   a.start_date, a.end_date,
                   c.category_name,
                   ua.full_name AS fundraiser_name,
                   ua.contact_num AS fundraiser_phone,
                   (
                       SELECT COUNT(*)
                       FROM activity_view av
                       WHERE av.activity_id = a.activity_id
                   ) AS view_count,
                   (
                       SELECT COUNT(*)
                       FROM favourite_list fl
                       WHERE fl.activity_id = a.activity_id
                   ) AS favourite_count
            FROM favourite_list f
            JOIN fundraising_activity a
              ON f.activity_id = a.activity_id
            JOIN category c
              ON a.category_id = c.category_id
            JOIN user_account ua
              ON a.account_id = ua.account_id
            WHERE f.account_id = ?
            ORDER BY f.favourite_id
            """,
            (accountId,)
        )

        rows = cursor.fetchall()
        connection.close()

        return [cls.fromRow(row) for row in rows]

    # SEARCH
    @classmethod
    def searchFavouritesByAccountId(cls, accountId: int, searchTerm: str) -> List["FavouriteList"]:
        connection = get_connection()
        keyword = f"%{searchTerm.strip()}%"

        cursor = connection.execute(
            """
            SELECT f.*, a.activity_name, a.activity_desc,
                   a.activity_status, a.category_id,
                   a.funding_current, a.funding_goal,
                   a.start_date, a.end_date,
                   c.category_name,
                   ua.full_name AS fundraiser_name,
                   ua.contact_num AS fundraiser_phone,
                   (
                       SELECT COUNT(*)
                       FROM activity_view av
                       WHERE av.activity_id = a.activity_id
                   ) AS view_count,
                   (
                       SELECT COUNT(*)
                       FROM favourite_list fl
                       WHERE fl.activity_id = a.activity_id
                   ) AS favourite_count
            FROM favourite_list f
            JOIN fundraising_activity a
              ON f.activity_id = a.activity_id
            JOIN category c
              ON a.category_id = c.category_id
            JOIN user_account ua
              ON a.account_id = ua.account_id
            WHERE f.account_id = ?
              AND (LOWER(a.activity_name) LIKE LOWER(?)
                   OR LOWER(a.activity_desc) LIKE LOWER(?))
            ORDER BY f.favourite_id
            """,
            (accountId, keyword, keyword)
        )

        rows = cursor.fetchall()
        connection.close()

        return [cls.fromRow(row) for row in rows]
