from dataclasses import dataclass
from calendar import monthrange
from datetime import date
from typing import Optional
from db import get_connection

@dataclass
class PlatformReport:
    reportType: str
    reportTitle: str
    startDate: str
    endDate: str
    totalDonationsCollected: float
    totalUserLogins: int
    totalActiveFundraisingActivities: int
    totalCompletedActivities: int
    mostActiveCategory: Optional[str]

    @classmethod
    def generateDailyReport(cls, selectedDate: str) -> "PlatformReport":
        return cls.generateReportInDateRange(
            reportType = "daily",
            reportTitle = f"Daily Report: {selectedDate}",
            startDate = selectedDate,
            endDate = selectedDate
        )

    @classmethod
    def generateWeeklyReport(cls, dateFrom: str, dateTo: str) -> "PlatformReport":
        return cls.generateReportInDateRange(
            reportType="weekly",
            reportTitle=f"Weekly Report ({dateFrom} to {dateTo})",
            startDate=dateFrom,
            endDate=dateTo
        )

    @classmethod
    def generateMonthlyReport(cls, selectedMonth: int, selectedYear: int) -> "PlatformReport":
        startDate = date(selectedYear, selectedMonth, 1).isoformat()
        endDate = date(selectedYear, selectedMonth, monthrange(selectedYear, selectedMonth)[1]).isoformat()

        return cls.generateReportInDateRange(
            reportType="monthly",
            reportTitle=f"Monthly Report ({selectedYear}-{selectedMonth:02d})",
            startDate=startDate,
            endDate=endDate
        )

    @classmethod
    def generateReportInDateRange(cls, reportType: str, reportTitle: str, startDate: str, endDate: str) -> "PlatformReport":
        connection = get_connection()
        donationsRow = connection.execute(
            """
            SELECT COALESCE(SUM(donation_amount), 0) AS total_donations
            FROM donation
            WHERE donation_date BETWEEN ? AND ?
            """,
            (startDate, endDate)
        ).fetchone()

        loginsRow = connection.execute(
            """
            SELECT COUNT(*) AS total_logins
            FROM user_session
            WHERE DATE(login_at) BETWEEN ? AND ?
            """,
            (startDate, endDate)
        ).fetchone()

        activeActivitiesRow = connection.execute(
            """
            SELECT COUNT(*) AS total_active
            FROM fundraising_activity
            WHERE activity_status = 'ongoing'
                AND start_date <= ?
                AND end_date >= ?
            """,
            (endDate, startDate)
        ).fetchone()

        completedActivitiesRow = connection.execute(
            """
            SELECT COUNT(*) AS total_completed
            FROM fundraising_activity
            WHERE activity_status = 'completed'
                AND end_date BETWEEN ? AND ?
            """,
            (startDate, endDate)
        ).fetchone()

        categoryRow = connection.execute(
            """
            SELECT c.category_name,
                   COALESCE(SUM(d.donation_amount), 0) AS total_amount
            FROM donation d
            JOIN fundraising_activity fa
                ON d.activity_id = fa.activity_id
            JOIN category c
                ON fa.category_id = c.category_id
            WHERE d.donation_date BETWEEN ? AND ?
            GROUP BY c.category_id, c.category_name
            ORDER BY total_amount DESC, c.category_name ASC
            LIMIT 1
            """,
            (startDate, endDate)
        ).fetchone()

        connection.close()
        return cls(
            reportType=reportType,
            reportTitle=reportTitle,
            startDate=startDate,
            endDate=endDate,
            totalDonationsCollected=float(donationsRow["total_donations"]),
            totalUserLogins=int(loginsRow["total_logins"]),
            totalActiveFundraisingActivities=int(activeActivitiesRow["total_active"]),
            totalCompletedActivities=int(completedActivitiesRow["total_completed"]),
            mostActiveCategory=categoryRow["category_name"] if categoryRow else None,
        )
