from flask import Blueprint, flash, redirect, render_template, request, url_for, session
from control.search_fundraising_activity_controller import search_fundraising_activity_controller
from control.create_fundraising_activity_controller import create_fundraising_activity_controller
from control.view_fundraising_activity_controller import view_fundraising_activity_controller
from control.update_fundraising_activity_controller import update_fundraising_activity_controller
from control.delete_fundraising_activity_controller import delete_fundraising_activity_controller
from control.view_completed_activity_controller import view_completed_activity_controller
from control.search_completed_activity_controller import search_completed_activity_controller
from control.view_my_donation_controller import view_my_donation_controller
from control.search_my_donation_controller import search_my_donation_controller
from control.view_fundraising_category_controller import view_fundraising_category_controller
from control.fundraising_activity_view_record_controller import fundraising_activity_view_record_controller
from control.view_favourite_list_controller import view_favourite_list_controller
from control.search_favourite_list_controller import search_favourite_list_controller
from boundary.access_control import login_required, roles_required, DONOR, FUNDRAISER, PLATFORM_MANAGEMENT


fundraising_activity_bp = Blueprint("fundraising_activity", __name__)


@fundraising_activity_bp.route("/activities/home")
def home():
    return redirect(url_for('fundraising_activity.list_activities'))

# LIST + SEARCH
@fundraising_activity_bp.route("/activities")
def list_activities():
    profile_id = session.get("profile_id")
    account_id = session.get("account_id")
    active_tab = request.args.get("tab", "browse").strip().lower()
    if profile_id != DONOR:
        active_tab = "browse"
    elif active_tab not in ["browse", "favourites", "history"]:
        active_tab = "browse"

    search_term = request.args.get("search", "")
    search_completed_term = request.args.get("searchCompleted", "")
    favourites = []
    donations = []
    categories = []
    categoryId = request.args.get("categoryId", "").strip()
    dateFrom = request.args.get("dateFrom", "").strip()
    dateTo = request.args.get("dateTo", "").strip()
    amountMin = request.args.get("amountMin", "").strip()
    amountMax = request.args.get("amountMax", "").strip()

    if active_tab == "favourites":
        viewController = view_favourite_list_controller()
        searchController = search_favourite_list_controller()
        favourites = viewController.viewFavourites(account_id)

        if "search" in request.args:
            if search_term.strip():
                favourites = searchController.searchFavourites(account_id, search_term)
            else:
                flash("Activity name or description required.", "error")

        if not favourites:
            flash("No favourite activities found.", "error")

        activities = []

    elif active_tab == "history":
        viewController = view_my_donation_controller()
        searchController = search_my_donation_controller()
        cateController = view_fundraising_category_controller()
        categories = cateController.viewFundraisingCategory()
        has_filter = bool(search_term or categoryId or dateFrom or dateTo or amountMin or amountMax)

        if has_filter:
            donations = searchController.searchMyDonations(
                account_id,
                search_term,
                categoryId,
                dateFrom,
                dateTo,
                amountMin,
                amountMax
            )
        else:
            donations = viewController.viewMyDonations(account_id)

        if dateFrom and dateTo and dateFrom > dateTo:
            flash("Invalid date range.", "error")

        if not donations:
            flash("No donations found.", "error")

        activities = []

    elif "search" in request.args:
        if search_term.strip():
            searchController = search_fundraising_activity_controller()
            if profile_id == FUNDRAISER:
                activities = searchController.searchActivitiesByAccountId(account_id, search_term)
            else:
                activities = searchController.searchActivities(search_term)
        else:
            flash("Activity name or description required.", "error")
            controller = view_fundraising_activity_controller()
            if profile_id == FUNDRAISER:
                activities = controller.viewActivitiesByAccountId(account_id)
            else:
                activities = controller.viewActivities()

    elif "searchCompleted" in request.args:
        if search_completed_term.strip():
            searchCompletedController = search_completed_activity_controller()
            activities = searchCompletedController.searchCompletedActivities(search_completed_term)
        else:
            flash("Activity name or description required.", "error")
            controller = view_completed_activity_controller()
            activities = controller.viewCompletedActivities()
    else:
        controller = view_fundraising_activity_controller()
        if profile_id == FUNDRAISER:
            activities = controller.viewActivitiesByAccountId(account_id)
        else:
            activities = controller.viewActivities()
    
    return render_template(
        "activities/list_activities.html",
        activities=activities,
        active_tab=active_tab,
        favourites=favourites,
        donations=donations,
        categories=categories,
        search_term=search_term,
        search_completed_term=search_completed_term,
        categoryId=categoryId,
        dateFrom=dateFrom,
        dateTo=dateTo,
        amountMin=amountMin,
        amountMax=amountMax
    )

# CREATE
@fundraising_activity_bp.route("/activities/create", methods=["GET", "POST"])
@roles_required(PLATFORM_MANAGEMENT, FUNDRAISER)
def create_activity():
    controller = create_fundraising_activity_controller()
    cateController = view_fundraising_category_controller()
    categories = cateController.viewFundraisingCategory()

    if request.method == "POST":
        account_id = request.form.get("accountId", "").strip()
        category_id = request.form.get("categoryId", "").strip()
        name = request.form.get("name", "").strip()
        desc = request.form.get("desc", "").strip()
        goal = request.form.get("goal", "").strip()
        start_date = request.form.get("startDate", "").strip()
        end_date = request.form.get("endDate", "").strip()

        if not account_id:
            flash("Account ID is required.", "error")
            return render_template("activities/create_activity.html" , categories=categories)

        if not category_id:
            flash("Category ID is required.", "error")
            return render_template("activities/create_activity.html" , categories=categories)

        if not name:
            flash("Activity name is required.", "error")
            return render_template("activities/create_activity.html" , categories=categories)

        if not goal:
            flash("Funding goal is required.", "error")
            return render_template("activities/create_activity.html" , categories=categories)

        try:
            account_id = int(account_id)
            category_id = int(category_id)
            goal = float(goal)
        except ValueError:
            flash("Invalid numeric input.", "error")
            return render_template("activities/create_activity.html" , categories=categories)

        success, message = controller.createActivity(
            account_id, category_id, name, desc, goal, start_date, end_date
        )

        if success:
            flash(message, "success")
            return redirect(url_for("fundraising_activity.list_activities"))

        flash(message, "error")

    return render_template("activities/create_activity.html", categories=categories)

# VIEW
@fundraising_activity_bp.route("/activities/view")
def view_activity():
    controller = view_fundraising_activity_controller()
    activities = controller.viewActivities()

    if not activities:
        flash("No activities found.", "error")
        return render_template("activities/view_activity.html")

    return render_template("activities/view_activity.html", activities=activities)


# UPDATE
@fundraising_activity_bp.route("/activities/update", methods=["GET", "POST"])
@roles_required(PLATFORM_MANAGEMENT, FUNDRAISER)
def update_activity():
    controller = update_fundraising_activity_controller()
    view_controller = view_fundraising_activity_controller()
    activity = None

    selected_activity_id = request.args.get("activityId", "").strip()
    if selected_activity_id:
        try:
            activity = view_controller.viewActivityById(int(selected_activity_id))
        except ValueError:
            flash("Invalid activity ID.", "error")
            return render_template("activities/update_activity.html", activity=activity)

        if not activity:
            flash("Activity ID does not exist.", "error")

    if request.method == "POST":
        activity_id = request.form.get("activityId", "").strip()
        name = request.form.get("name", "").strip()
        desc = request.form.get("desc", "").strip()
        goal = request.form.get("goal", "").strip()
        status = request.form.get("status", "").strip()

        if not activity_id:
            flash("Activity ID is required.", "error")
            return render_template("activities/update_activity.html", activity=activity)

        try:
            activity_id = int(activity_id)
        except ValueError:
            flash("Invalid activity ID.", "error")
            return render_template("activities/update_activity.html", activity=activity)

        activity = view_controller.viewActivityById(activity_id)
        if not activity:
            flash("Activity ID does not exist.", "error")
            return render_template("activities/update_activity.html", activity=activity)

        if not name:
            flash("Activity name is required.", "error")
            return render_template("activities/update_activity.html", activity=activity)

        if not goal:
            flash("Funding goal is required.", "error")
            return render_template("activities/update_activity.html", activity=activity)

        if not status:
            flash("Status is required.", "error")
            return render_template("activities/update_activity.html", activity=activity)

        try:
            goal = float(goal)
        except ValueError:
            flash("Invalid numeric input.", "error")
            return render_template("activities/update_activity.html", activity=activity)

        success, message = controller.updateActivity(
            activity_id, name, desc, goal, status
        )

        if success:
            flash(message, "success")
            return redirect(url_for("fundraising_activity.list_activities"))

        flash(message, "error")

    return render_template("activities/update_activity.html", activity=activity)


# DELETE
@fundraising_activity_bp.route("/activities/delete", methods=["GET", "POST"])
@roles_required(PLATFORM_MANAGEMENT, FUNDRAISER)
def delete_activity():
    controller = delete_fundraising_activity_controller()

    if request.method == "POST":
        activity_id = request.form.get("activityId", "").strip()

        if not activity_id:
            flash("Activity ID is required.", "error")
            return render_template("activities/delete_activity.html")

        success, message = controller.deleteActivity(activity_id)

        if success:
            flash(message, "success")
            return redirect(url_for("fundraising_activity.list_activities"))

        flash(message, "error")

    return render_template("activities/delete_activity.html")

# VIEW COMPLETED ACTIVITIES
@fundraising_activity_bp.route("/activities/viewCompleted")
@roles_required(FUNDRAISER, PLATFORM_MANAGEMENT)
def view_completed_activities():
    profile_id = session.get("profile_id")
    account_id = session.get("account_id")
    search_term = request.args.get("search", "").strip()
    categoryId = request.args.get("categoryId", "").strip()
    dateFrom = request.args.get("dateFrom", "").strip()
    dateTo = request.args.get("dateTo", "").strip()
    cate_controller = view_fundraising_category_controller()
    view_controller = view_completed_activity_controller()
    search_controller = search_completed_activity_controller()
    categories = cate_controller.viewFundraisingCategory()
    has_filter = bool(search_term or categoryId or dateFrom or dateTo)

    if has_filter:
        if profile_id == FUNDRAISER:
            activities = search_controller.searchCompletedActivitiesByAccountId(
                account_id,
                search_term,
                categoryId,
                dateFrom,
                dateTo
            )
        else:
            activities = search_controller.searchCompletedActivities(
                search_term,
                categoryId,
                dateFrom,
                dateTo
            )
    else:
        if profile_id == FUNDRAISER:
            activities = view_controller.viewCompletedActivitiesByAccountId(account_id)
        else:
            activities = view_controller.viewCompletedActivities()

    if dateFrom and dateTo and dateFrom > dateTo:
        flash("Invalid date range.", "error")
        return render_template(
            "activities/view_completed_activity.html",
            activities=activities,
            search_term=search_term,
            categoryId=categoryId,
            dateFrom=dateFrom,
            dateTo=dateTo,
            categories=categories
        )

    if not activities:
        flash("No activities found.", "error")

    return render_template(
        "activities/view_completed_activity.html",
        activities=activities,
        search_term=search_term,
        categoryId=categoryId,
        dateFrom=dateFrom,
        dateTo=dateTo,
        categories=categories
    )

# View and Search My Donations
@fundraising_activity_bp.route("/activities/myDonations")
@login_required
def view_my_donations():
    if session.get("profile_id") == DONOR:
        query_args = request.args.to_dict()
        query_args["tab"] = "history"
        return redirect(url_for("fundraising_activity.list_activities", **query_args))

    account_id = session.get("account_id")
    search_term = request.args.get("search", "").strip()
    categoryId = request.args.get("categoryId", "").strip()
    dateFrom = request.args.get("dateFrom", "").strip()
    dateTo = request.args.get("dateTo", "").strip()
    amountMin = request.args.get("amountMin", "").strip()
    amountMax = request.args.get("amountMax", "").strip()
    viewController = view_my_donation_controller()
    searchController = search_my_donation_controller()
    cateController = view_fundraising_category_controller()
    categories = cateController.viewFundraisingCategory()
    has_filter = bool(search_term or categoryId or dateFrom or dateTo or amountMin or amountMax)

    if has_filter:
        donations = searchController.searchMyDonations(account_id, search_term, categoryId, dateFrom, dateTo, amountMin, amountMax)

    else:
        donations = viewController.viewMyDonations(account_id)

    if dateFrom and dateTo and dateFrom > dateTo:
        flash("Invalid date range.", "error")
        
        return render_template(
        "activities/view_my_donations.html", 
        donations=donations, 
        search_term=search_term, 
        categoryId=categoryId,
        dateFrom=dateFrom,
        dateTo=dateTo,
        amountMin=amountMin,
        amountMax=amountMax,
        categories=categories)
    
    if not donations:
        flash("No donations found.", "error")

    return render_template(
        "activities/view_my_donations.html", 
        donations=donations, 
        search_term=search_term, 
        categoryId=categoryId,
        dateFrom=dateFrom,
        dateTo=dateTo,
        amountMin=amountMin,
        amountMax=amountMax,
        categories=categories)

# Record Activity View
@fundraising_activity_bp.route("/activities/recordView/<int:activity_id>", methods=["POST"])
@login_required
def record_activity_view(activity_id):
    account_id = session.get("account_id")

    controller = fundraising_activity_view_record_controller()
    controller.recordActivityView(account_id, activity_id)

    return "", 204
