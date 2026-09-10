from flask import Blueprint, flash, redirect, render_template, request, url_for
from control.search_user_account_controller import search_user_account_controller
from control.create_user_account_controller import create_user_account_controller
from control.view_user_account_controller import view_user_account_controller
from control.update_user_account_controller import update_user_account_controller
from control.suspend_user_account_controller import suspend_user_account_controller
from entity.user_account import UserAccount
from entity.user_profile import UserProfile
from boundary.access_control import roles_required, USER_ADMIN

user_account_bp = Blueprint('user_account', __name__)

@user_account_bp.route('/accounts')
@roles_required(USER_ADMIN)
def list_accounts():
    search_term = request.args.get("search", "")
    profiles = UserProfile.getAllProfiles()

    if "search" in request.args:
        if search_term.strip():
            controller = search_user_account_controller()
            accounts = controller.searchAccounts(search_term)
        else:
            flash("Account search term is required.", "error")
            controller = view_user_account_controller()
            accounts = controller.viewUserAccount()
    else:
        controller = view_user_account_controller()
        accounts = controller.viewUserAccount()

    return render_template(
        "accounts/list_accounts.html",
        accounts = accounts,
        search_term = search_term,
        profiles = profiles
    )
@user_account_bp.route('/accounts/view')
@roles_required(USER_ADMIN)
def view_accounts():
    return redirect(url_for("user_account.list_accounts"))

@user_account_bp.route("/accounts/create", methods=["GET","POST"])
@roles_required(USER_ADMIN)
def create_accounts():
    controller = create_user_account_controller()
    profiles = UserProfile.getAllProfiles()

    if request.method == "POST":
        full_name = request.form.get("full_name", "").strip()
        user_name = request.form.get("userName", "").strip()
        password = request.form.get("passWord", "").strip()
        birthday = request.form.get("birthday", "").strip()
        address = request.form.get("address", "").strip()
        contact_number = request.form.get("contact_number", "").strip()
        profile_id = request.form.get("profileId", "").strip()

        if not full_name:
            flash("Full name is required.", "error")
            return redirect(url_for("user_account.list_accounts"))

        if not user_name:
            flash("User name is required.", "error")
            return redirect(url_for("user_account.list_accounts"))

        if not password:
            flash("Password is required.", "error")
            return redirect(url_for("user_account.list_accounts"))

        if not contact_number:
            flash("Contact number is required.", "error")
            return redirect(url_for("user_account.list_accounts"))

        if not profile_id:
            flash("Profile is required.", "error")
            return redirect(url_for("user_account.list_accounts"))

        success, message = controller.createUserAccount(
            full_name,
            user_name,
            password,
            birthday,
            address,
            contact_number,
            int(profile_id),
            "ACTIVE"
        )

        if success:
            flash(message, "success")
            return redirect(url_for("user_account.list_accounts"))
        flash(message, "error")
        return redirect(url_for("user_account.list_accounts"))

    return redirect(url_for("user_account.list_accounts"))

@user_account_bp.route("/accounts/update", methods=["GET","POST"])
@roles_required(USER_ADMIN)
def update_accounts():
    controller = update_user_account_controller()
    profiles = UserProfile.getAllProfiles()

    if request.method == "POST":
        account_id = request.form.get("accountId", "").strip()
        full_name = request.form.get("fullName", "").strip()
        user_name = request.form.get("userName", "").strip()
        password = request.form.get("password", "").strip()
        birthday = request.form.get("birthday", "").strip()
        address = request.form.get("address", "").strip()
        contact_number = request.form.get("contactNumber", "").strip()
        profile_id = request.form.get("profileId", "").strip()
        account_status = request.form.get("accountStatus", "").strip()

        if not account_id:
            flash("Account ID is required.", "error")
            return redirect(url_for("user_account.list_accounts"))

        if not full_name:
            flash("Full name is required.", "error")
            return redirect(url_for("user_account.list_accounts"))

        if not user_name:
            flash("Username is required.", "error")
            return redirect(url_for("user_account.list_accounts"))

        if not password:
            flash("Password is required.", "error")
            return redirect(url_for("user_account.list_accounts"))

        if not contact_number:
            flash("Contact number is required.", "error")
            return redirect(url_for("user_account.list_accounts"))

        if not profile_id:
            flash("Profile is required.", "error")
            return redirect(url_for("user_account.list_accounts"))

        if not account_status:
            flash("Account status is required.", "error")
            return redirect(url_for("user_account.list_accounts"))

        success, message = controller.updateUserAccount(
            int(account_id),
            full_name,
            user_name,
            password,
            birthday,
            address,
            contact_number,
            int(profile_id),
            account_status
        )

        if success:
            flash(message, "success")
            return redirect(url_for("user_account.list_accounts"))
        flash(message, "error")
        return redirect(url_for("user_account.list_accounts"))
    return redirect(url_for("user_account.list_accounts"))

@user_account_bp.route("/accounts/suspend", methods=["GET", "POST"])
@roles_required(USER_ADMIN)
def suspend_account():
    controller = suspend_user_account_controller()

    if request.method == "POST":
        account_id = request.form.get("accountId", "").strip()

        if not account_id:
            flash("Account ID is required.", "error")
            return render_template("accounts/suspend_account.html")
        success, message = controller.suspendUserAccount(int(account_id))

        if success:
            flash(message, "success")
            return redirect(url_for("user_account.list_accounts"))

        flash(message, "error")

    return redirect(url_for("user_account.list_accounts"))
