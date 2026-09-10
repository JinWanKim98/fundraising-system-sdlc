from flask import Flask
from auth_routes import auth_bp

app = Flask(__name__)
app.secret_key = "supersecretkey"  # Required for session management

# Register the blueprint
app.register_blueprint(auth_bp)

if __name__ == "__main__":
    app.run(debug=True)