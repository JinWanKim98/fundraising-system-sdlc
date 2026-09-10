from flask import Blueprint, flash, render_template, request
from boundary.access_control import roles_required, PLATFORM_MANAGEMENT
from control.view_platform_report_controller import view_platform_report_controller


platform_report_bp = Blueprint('platform_report', __name__)


@platform_report_bp.route("/reports")
@roles_required(PLATFORM_MANAGEMENT)
def view_reports():
    reportType = request.args.get("type", "daily").strip().lower()
    controller = view_platform_report_controller()
    report = None

    if reportType not in ["daily", "weekly", "monthly"]:
        reportType = "daily"
        flash("Invalid report type.", "error")

    dailyDate = request.args.get("dailyDate", "").strip()
    weeklyFrom = request.args.get("weeklyFrom", "").strip()
    weeklyTo = request.args.get("weeklyTo", "").strip()
    monthlyMonth = request.args.get("monthlyMonth", "").strip()
    monthlyYear = request.args.get("monthlyYear", "").strip()

    shouldGenerate = "generate" in request.args

    if shouldGenerate:
        if reportType == "daily":
            success, message, report = controller.generateDailyReport(dailyDate)
        elif reportType == "weekly":
            success, message, report = controller.generateWeeklyReport(weeklyFrom, weeklyTo)
        else:
            success, message, report = controller.generateMonthlyReport(monthlyMonth, monthlyYear)

        flash(message, "success" if success else "error")

    return render_template(
        "reports/platform_reports.html",
        active_tab=reportType,
        report=report,
        daily_date=dailyDate,
        weekly_from=weeklyFrom,
        weekly_to=weeklyTo,
        monthly_month=monthlyMonth,
        monthly_year=monthlyYear
    )
