from flask import Blueprint, flash, redirect, render_template, request, url_for
from control.search_user_profile_controller import search_user_profile_controller
from control.create_user_profile_controller import create_user_profile_controller
from control.view_user_profile_controller import view_user_profile_controller
from control.update_user_profile_controller import update_user_profile_controller
from control.delete_user_profile_controller import delete_user_profile_controller
from boundary.access_control import login_required, roles_required, USER_ADMIN

user_profile_bp = Blueprint("user_profile", __name__)

@user_profile_bp.route("/profiles/home")
@roles_required(USER_ADMIN)
def home():
    return redirect(url_for('user_profile.list_profiles'))

@user_profile_bp.route("/profiles")
@roles_required(USER_ADMIN)
def list_profiles():
    search_term = request.args.get("search", "")

    if "search" in request.args:
        if search_term.strip():
            controller = search_user_profile_controller()
            profiles = controller.searchProfiles(search_term)

        else:
            flash("Profile name or description needs to be provided.", "error")
            controller = view_user_profile_controller()
            profiles = controller.viewUserProfile()
    else:
        controller = view_user_profile_controller()
        profiles = controller.viewUserProfile()
    return render_template(
        "profiles/list_profiles.html",
        profiles = profiles,
        search_term = search_term
    )


@user_profile_bp.route("/profiles/create", methods=["GET", "POST"])
@roles_required(USER_ADMIN)
def create_profile():
    controller = create_user_profile_controller()

    if request.method == "POST":
        profile_name = request.form.get("profileName", "").strip()
        profile_description = request.form.get("profileDescription", "").strip()

        if not profile_name:
            flash("Profile name is required.", "error")
            return redirect(url_for("user_profile.list_profiles"))
        
        if not profile_description:
            flash("Profile description is required.", "error")
            return redirect(url_for("user_profile.list_profiles"))
                
        success, message = controller.createUserProfile(
            profile_name,
            profile_description
        )
        if success:
            flash(message, "success")
            return redirect(url_for("user_profile.list_profiles"))

        flash(message, "error")
        return redirect(url_for("user_profile.list_profiles"))

    return redirect(url_for("user_profile.list_profiles"))

@user_profile_bp.route("/profiles/view")
@roles_required(USER_ADMIN)
def view_profile():
    return redirect(url_for("user_profile.list_profiles"))


@user_profile_bp.route("/profiles/update", methods=["GET", "POST"])
@roles_required(USER_ADMIN)
def update_profile():
    controller = update_user_profile_controller()

    if request.method == "POST":
        profile_id = request.form.get("profileId", "").strip()
        profile_name = request.form.get("profileName", "").strip()
        profile_description = request.form.get("profileDescription", "").strip()

        if not profile_id:
            flash("Profile ID is required.", "error")
            return redirect(url_for("user_profile.list_profiles"))
        
        if not profile_name:
            flash("Profile name is required.", "error")
            return redirect(url_for("user_profile.list_profiles"))
        
        if not profile_description:
            flash("Profile description is required.", "error")
            return redirect(url_for("user_profile.list_profiles"))   
             
        success, message = controller.updateUserProfile(
            profile_id,
            profile_name,
            profile_description
        )

        if success:
            flash(message, "success")
            return redirect(url_for("user_profile.list_profiles"))

        flash(message, "error")
        return redirect(url_for("user_profile.list_profiles"))

    return redirect(url_for("user_profile.list_profiles"))

@user_profile_bp.route("/profiles/delete", methods=["GET", "POST"])
@roles_required(USER_ADMIN)
def delete_profile():
    controller = delete_user_profile_controller()

    if request.method == "POST":
        profile_id = request.form.get("profileId", "").strip()

        if not profile_id:
            flash("Profile ID is required.", "error")
            return render_template("profiles/delete_profile.html")
             
        success, message = controller.deleteUserProfile(
            profile_id,
        )

        if success:
            flash(message, "success")
            return redirect(url_for("user_profile.list_profiles"))

        flash(message, "error")

    return redirect(url_for("user_profile.list_profiles"))
