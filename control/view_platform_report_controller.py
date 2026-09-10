from typing import Optional, Tuple
from entity.platform_report import PlatformReport

class view_platform_report_controller:
    """
    Control class responsible for generating platform reports.
    """
    def generateDailyReport(self, selectedDate: str) -> Tuple[bool, str, Optional[PlatformReport]]:
        if not selectedDate:
            return False, "Date is required.", None

        report = PlatformReport.generateDailyReport(selectedDate)
        return True, "Daily report generated successfully", report

    def generateWeeklyReport(self, dateFrom: str, dateTo: str) -> Tuple[bool, str, Optional[PlatformReport]]:
        if not dateFrom or not dateTo:
            return False, "Date range is required.", None
        if dateFrom > dateTo:
            return False, "Invalid date range.", None

        report = PlatformReport.generateWeeklyReport(dateFrom, dateTo)
        return True, "Weekly report generated successfully", report

    def generateMonthlyReport(self, selectedMonth: str, selectedYear: str) -> Tuple[bool, str, Optional[PlatformReport]]:
        if not selectedMonth or not selectedYear:
            return False, "Month and year required.", None

        try:
            monthValue = int(selectedMonth)
            yearValue = int(selectedYear)
        except ValueError:
            return False, "Month and year must be numeric", None

        if monthValue < 1 or monthValue > 12:
            return False, "Invalid month.", None
        report = PlatformReport.generateMonthlyReport(monthValue, yearValue)
        return True, "Monthly report generated successfully", report