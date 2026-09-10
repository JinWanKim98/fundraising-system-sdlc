from functools import wraps
from flask import flash, redirect, session, url_for
USER_ADMIN = 1
FUNDRAISER = 2
DONOR = 3
PLATFORM_MANAGEMENT = 4

def roles_required(*allowed_profile_ids):
    def decorator(view_function):
        @wraps(view_function)
        def wrapped_view(*args, **kwargs):
            if not session.get("account_id"):
                flash("Please log in to continue.", "error")
                return redirect(url_for("auth.login"))
            profile_id = session.get("profile_id")
            if profile_id not in allowed_profile_ids:
                flash("You do not have permission to access this page.", "error")
                return redirect(url_for("home"))
            return view_function(*args, **kwargs)
        return wrapped_view
    return decorator



def login_required(view_function):
    """
    keeps access to log in users
    """
    @wraps(view_function)
    def wrapped_view(*args, **kwargs):
        if not session.get("account_id"):
            flash("Please log in to continue.", "error")
            return redirect(url_for("auth.login"))
        return view_function(*args, **kwargs)
    return wrapped_view
