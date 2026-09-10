from flask import Flask, redirect, session, url_for
from boundary.user_profile_routes import user_profile_bp
from boundary.fundraising_category_routes import fundraising_category_bp
from boundary.fundraising_activity_routes import fundraising_activity_bp
from boundary.user_account_routes import user_account_bp
from boundary.auth_routes import auth_bp, get_dashboard_endpoint
from boundary.favourite_list_routes import favourite_list_bp
from boundary.report_routes import platform_report_bp

def create_app():
    app = Flask(__name__)
    app.secret_key = "dev-secret-key"

    @app.route("/")
    def home():
        if not session.get("account_id"):
            return redirect(url_for("auth.login"))
        return redirect(url_for(get_dashboard_endpoint(session.get("profile_id"))))

    app.register_blueprint(user_profile_bp)
    app.register_blueprint(fundraising_category_bp)
    app.register_blueprint(fundraising_activity_bp)
    app.register_blueprint(user_account_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(favourite_list_bp)
    app.register_blueprint(platform_report_bp)

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
