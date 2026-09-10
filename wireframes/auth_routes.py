from flask import Blueprint, render_template, request, redirect, url_for, session

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/", methods=["GET", "POST"])
@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    error = None
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        # Hardcoded credentials
        if username == "fundraiser" and password == "1234":
            session["username"] = "Rachel Tan"
            session["role"] = "fundraiser"
            return redirect(url_for("auth.fundraiser_activities"))
        elif username == "donor" and password == "1234":
            session["username"] = "David Lim"
            session["role"] = "donor"
            return redirect(url_for("auth.donor_browse"))
        elif username == "pm" and password == "1234":
            session["username"] = "Jayden Tan"
            session["role"] = "pm"
            return redirect(url_for("auth.pm_categories"))
        elif username == "admin" and password == "1234":
            session["username"] = "Chloe Lim"
            session["role"] = "admin"
            return redirect(url_for("auth.admin_accounts"))
        else:
            error = "Invalid username or password"

    return render_template("login.html", error=error)

# --- USER ADMIN ROUTES ---
@auth_bp.route("/admin/accounts")
def admin_accounts():
    if session.get("role") != "admin": return redirect(url_for("auth.login"))
    # Dummy data for the prototype
    accounts = [
        {"name": "Rachel Tan", "status": "Active"},
        {"name": "David Lim", "status": "Active"}
    ]
    return render_template("admin_user_account.html", accounts=accounts)

@auth_bp.route("/admin/profiles")
def admin_profiles():
    if session.get("role") != "admin": return redirect(url_for("auth.login"))
    # Dummy data for the prototype
    profiles = [
        {"profile_name": "Fundraiser", "description": "Can create and manage activities"},
        {"profile_name": "Donor", "description": "Can browse and donate to activities"}
    ]
    return render_template("admin_user_profile.html", profiles=profiles)

# --- FUNDRAISER ROUTES ---
@auth_bp.route("/fundraiser/activities")
def fundraiser_activities():
    if session.get("role") != "fundraiser": return redirect(url_for("auth.login"))
    return render_template("fundraiser_activities.html")

@auth_bp.route("/fundraiser/history")
def fundraiser_history():
    if session.get("role") != "fundraiser": return redirect(url_for("auth.login"))
    return render_template("fundraiser_history.html")

@auth_bp.route("/fundraiser/performance")
def fundraiser_performance():
    if session.get("role") != "fundraiser": return redirect(url_for("auth.login"))
    return render_template("fundraiser_performance.html")

@auth_bp.route("/fundraiser/analytics")
def fundraiser_analytics():
    if session.get("role") != "fundraiser": return redirect(url_for("auth.login"))
    return render_template("fundraiser_analytics.html")

@auth_bp.route("/fundraiser/create")
def fundraiser_create():
    return render_template("fundraiser_form.html", mode="Create")

@auth_bp.route("/fundraiser/edit")
def fundraiser_edit():
    return render_template("fundraiser_form.html", mode="Update")

# --- DONOR ROUTES ---
@auth_bp.route("/donor/browse")
def donor_browse():
    if session.get("role") != "donor": return redirect(url_for("auth.login"))
    return render_template("donor_browse.html")

@auth_bp.route("/donor/details")
def donor_details():
    if session.get("role") != "donor": return redirect(url_for("auth.login"))
    return render_template("donor_details.html")

@auth_bp.route("/donor/donate")
def donor_donate():
    if session.get("role") != "donor": return redirect(url_for("auth.login"))
    return render_template("donor_donate.html")

@auth_bp.route("/donor/favorites")
def donor_favorites():
    if session.get("role") != "donor": return redirect(url_for("auth.login"))
    return render_template("donor_favorites.html")

@auth_bp.route("/donor/history")
def donor_history():
    if session.get("role") != "donor": return redirect(url_for("auth.login"))
    return render_template("donor_history.html")

# --- PLATFORM MANAGEMENT ROUTES ---
@auth_bp.route("/pm/categories")
def pm_categories():
    if session.get("role") != "pm": return redirect(url_for("auth.login"))
    return render_template("pm_main_categories.html")

@auth_bp.route("/pm/create_category")
def pm_create_category():
    if session.get("role") != "pm": return redirect(url_for("auth.login"))
    return render_template("pm_category_form.html", mode="Create")

@auth_bp.route("/pm/edit_category")
def pm_edit_category():
    if session.get("role") != "pm": return redirect(url_for("auth.login"))
    return render_template("pm_category_form.html", mode="Update")

@auth_bp.route("/pm/reports")
def pm_reports():
    if session.get("role") != "pm": return redirect(url_for("auth.login"))
    return render_template("pm_reports.html")

@auth_bp.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("auth.login"))