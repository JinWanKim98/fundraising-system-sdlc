from flask import Blueprint, flash, redirect, render_template, request, session, url_for

from boundary.access_control import (
    DONOR,
    FUNDRAISER,
    PLATFORM_MANAGEMENT,
    USER_ADMIN,
)
from control.login_controller import login_controller
from control.logout_controller import logout_controller
from entity.user_profile import UserProfile

"""
Flow is: /login GET -> show form
/login POST -> authenticate + create session + store Flask session
/logout -> update DB session + clear Flask session
"""

auth_bp = Blueprint('auth', __name__)


def get_dashboard_endpoint(profile_id):
    dashboard_endpoints = {
        USER_ADMIN: "user_account.list_accounts",
        FUNDRAISER: "fundraising_activity.list_activities",
        DONOR: "fundraising_activity.list_activities",
        PLATFORM_MANAGEMENT: "fundraising_category.main_page",
    }
    return dashboard_endpoints.get(profile_id, "auth.login")

@auth_bp.route("/login", methods=['GET', 'POST'])

def login():
    if session.get("account_id"):
        dashboard_endpoint = get_dashboard_endpoint(session.get("profile_id"))
        if dashboard_endpoint != "auth.login":
            return redirect(url_for(dashboard_endpoint))
        session.clear()

    controller = login_controller()
    profiles = UserProfile.getAllProfiles()

    if request.method == "POST":
        user_name = request.form.get("userName", "").strip()
        password = request.form.get("passWord", "").strip()
        selected_profile_id = request.form.get("profileId", "").strip()

        if not selected_profile_id:
            flash("Profile is required.", "error")
            return render_template("auth/login.html", profiles=profiles)

        try:
            selected_profile_id = int(selected_profile_id)
        except ValueError:
            flash("Invalid profile selected.", "error")
            return render_template("auth/login.html", profiles=profiles)

        success, message, account, user_session = controller.loginUser(user_name, password)

        if success:
            if account.profileId != selected_profile_id:
                logout_controller().logoutUser(user_session.sessionId)
                flash("Selected profile does not match this account.", "error")
                return render_template("auth/login.html", profiles=profiles)

            session["account_id"] = account.accountId
            session["profile_id"] = account.profileId
            session["user_name"] = account.userName
            session["session_id"] = user_session.sessionId

            flash(message, "success")
            return redirect(url_for(get_dashboard_endpoint(account.profileId)))

        flash(message, "error")
    return render_template("auth/login.html", profiles=profiles)

@auth_bp.route("/logout")
def logout():
    controller = logout_controller()
    session_id = session.get("session_id")

    if session_id:
        success, message = controller.logoutUser(session_id)
        flash(message, "success" if success else "error")

    session.clear()
    return redirect(url_for("auth.login"))
