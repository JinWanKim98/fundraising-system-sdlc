from flask import Blueprint, request, session, redirect, url_for, jsonify
from control.add_favourite_list_controller import add_favourite_list_controller
from boundary.access_control import login_required, roles_required, DONOR


favourite_list_bp = Blueprint("favourites_list", __name__)


# =========================
# VIEW FAVOURITES
# =========================
@favourite_list_bp.route("/favourites/view")
@login_required
@roles_required(DONOR)
def view_favourites_list():
    query_args = request.args.to_dict()
    query_args["tab"] = "favourites"
    return redirect(url_for("fundraising_activity.list_activities", **query_args))


# =========================
# SEARCH FAVOURITES
# =========================
@favourite_list_bp.route("/favourites/search")
@login_required
@roles_required(DONOR)
def search_favourites_list():
    query_args = request.args.to_dict()
    query_args["tab"] = "favourites"
    return redirect(url_for("fundraising_activity.list_activities", **query_args))


# =========================
# ADD TO FAVOURITES
# =========================
@favourite_list_bp.route("/favourites/add", methods=["POST"])
@login_required
def add_favourite_list():
    if session.get("profile_id") != DONOR:
        return jsonify({
            "success": False,
            "message": "You do not have permission to access."
        }), 403

    account_id = session.get("account_id")
    activity_id = request.form.get("activityId")

    controller = add_favourite_list_controller()
    success, message = controller.addFavourite(account_id, activity_id)

    return jsonify({
        "success": success,
        "message": message
    })
