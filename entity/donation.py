from dataclasses import dataclass
from typing import List, Optional
from db import get_connection

@dataclass
class donation:
    """
    Entity class representing a donation.
    """
    donationId: Optional[int]
    accountId: int
    activityId: int
    donationAmount: float
    donationDate: str
    activityName: str
    activityCategory: str

    @classmethod
    def fromRow(cls, row) -> "donation":
        """
        Create a donation instance from a database row
        """
        return cls(
            donationId=row["donation_id"],
            accountId=row["account_id"],
            activityId=row["activity_id"],
            activityName=row["activity_name"],
            activityCategory=row["category_name"],
            donationAmount=row["donation_amount"],
            donationDate=row["donation_date"]
        )
    
    @classmethod
    def viewMyDonations(cls, accountId: int) -> List["donation"]:
        """
        Retrieve all donations from the database and return them as a list of donation instances.
        """
        connection = get_connection()
        cursor = connection.execute(
            """
            SELECT d.donation_id, d.account_id, d.activity_id, fra.activity_name, c.category_name, d.donation_amount, d.donation_date
            FROM donation d
            JOIN fundraising_activity fra ON d.activity_id = fra.activity_id
            JOIN category c ON fra.category_id = c.category_id
            WHERE d.account_id = ?
            """
        , (accountId,))

        rows = cursor.fetchall()
        connection.close()
        return [cls.fromRow(row) for row in rows]
    
    @classmethod
    def searchMyDonations(cls, accountId: int, searchTerm: str = "", categoryId: str = "", dateFrom: str = "", dateTo: str = "", amountMin: str = "", amountMax: str = "") -> List["donation"]:

        connection = get_connection()

        query = """
            SELECT
                d.donation_id,
                d.account_id,
                d.activity_id,
                fra.activity_name,
                c.category_name,
                d.donation_amount,
                d.donation_date
            FROM donation d
            JOIN fundraising_activity fra
                ON d.activity_id = fra.activity_id
            JOIN category c
                ON fra.category_id = c.category_id
            WHERE d.account_id = ?
        """

        params = [accountId]

        # keyword
        if searchTerm.strip():
            keyword = f"%{searchTerm.strip()}%"
            query += """
                AND (
                    LOWER(fra.activity_name) LIKE LOWER(?)
                    OR LOWER(c.category_name) LIKE LOWER(?)
                )
            """
            params.extend([keyword, keyword])

        # category
        if categoryId:
            query += """
                AND c.category_id = ?
            """
            params.append(categoryId)

        # date from
        if dateFrom:
            query += """
                AND d.donation_date >= ?
            """
            params.append(dateFrom)

        # date to
        if dateTo:
            query += """
                AND d.donation_date <= ?
            """
            params.append(dateTo)

        # amount min
        if amountMin:
            query += """
                AND d.donation_amount >= ?
            """
            params.append(amountMin)

        # amount max
        if amountMax:
            query += """
                AND d.donation_amount <= ?
            """
            params.append(amountMax)

        query += """
            ORDER BY d.donation_date DESC
        """

        cursor = connection.execute(query, tuple(params))

        rows = cursor.fetchall()

        connection.close()

        return [cls.fromRow(row) for row in rows]