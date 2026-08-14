import os
import re
import sqlite3
from datetime import timedelta
from functools import wraps

import bcrypt
from authlib.integrations.flask_client import OAuth
from dotenv import load_dotenv
from flask import Flask, jsonify, redirect, render_template, request, url_for
from flask_cors import CORS
from flask_jwt_extended import (
    JWTManager,
    create_access_token,
    get_jwt,
    get_jwt_identity,
    jwt_required,
)
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

load_dotenv()

app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("FLASK_SECRET_KEY", "change-this-secret")
app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY", "change-this-jwt-secret")
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(days=7)
app.config["JWT_TOKEN_LOCATION"] = ["headers"]
app.config["JWT_HEADER_NAME"] = "Authorization"
app.config["JWT_HEADER_TYPE"] = "Bearer"

# Enable CORS for all routes
CORS(app, resources={
    r"/api/*": {
        "origins": ["https://your-app.vercel.app", "http://localhost:3000", "http://localhost:5000", "http://127.0.0.1:3000", "http://127.0.0.1:5000"],
        "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        "allow_headers": ["Content-Type", "Authorization"]
    }
})

jwt = JWTManager(app)
limiter = Limiter(key_func=get_remote_address, app=app, default_limits=[])

oauth = OAuth(app)

# Google OAuth configuration. Add real values to .env before using this flow.
if os.getenv("GOOGLE_CLIENT_ID") and os.getenv("GOOGLE_CLIENT_SECRET"):
    oauth.register(
        name="google",
        client_id=os.getenv("GOOGLE_CLIENT_ID"),
        client_secret=os.getenv("GOOGLE_CLIENT_SECRET"),
        server_metadata_url="https://accounts.google.com/.well-known/openid-configuration",
        client_kwargs={"scope": "openid email profile"},
    )

# GitHub OAuth configuration. Add real values to .env before using this flow.
if os.getenv("GITHUB_CLIENT_ID") and os.getenv("GITHUB_CLIENT_SECRET"):
    oauth.register(
        name="github",
        client_id=os.getenv("GITHUB_CLIENT_ID"),
        client_secret=os.getenv("GITHUB_CLIENT_SECRET"),
        access_token_url="https://github.com/login/oauth/access_token",
        authorize_url="https://github.com/login/oauth/authorize",
        api_base_url="https://api.github.com/",
        client_kwargs={"scope": "user:email"},
    )

DB_PATH = "reviews.db"
EMAIL_RE = re.compile(r"^[^\s@]+@[^\s@]+\.[^\s@]+$")


def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db()
    conn.executescript(
        """
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT UNIQUE NOT NULL,
            password_hash BLOB NOT NULL,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        );

        CREATE TABLE IF NOT EXISTS revoked_tokens (
            jti TEXT PRIMARY KEY,
            revoked_at TEXT DEFAULT CURRENT_TIMESTAMP
        );

        CREATE TABLE IF NOT EXISTS reviews (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            review TEXT NOT NULL,
            sentiment TEXT NOT NULL,
            theme TEXT NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users(id)
        );
        """
    )
    conn.commit()
    conn.close()


def validate_credentials(email, password):
    errors = {}
    if not email or not EMAIL_RE.match(email):
        errors["email"] = "Enter a valid email address."
    if not password or len(password) < 8:
        errors["password"] = "Password must contain at least 8 characters."
    if password and len(password) > 128:
        errors["password"] = "Password must be 128 characters or fewer."
    return errors


def analyze_review(review):
    text = review.lower()
    positive_words = {"good", "great", "amazing", "excellent", "clean", "friendly", "nice"}
    negative_words = {"bad", "dirty", "poor", "terrible", "rude", "awful"}
    positive_hits = sum(word in text for word in positive_words)
    negative_hits = sum(word in text for word in negative_words)

    if positive_hits > negative_hits:
        sentiment = "Positive"
    elif negative_hits > positive_hits:
        sentiment = "Negative"
    else:
        sentiment = "Neutral"

    themes = [
        ("Food", "food"),
        ("Location", "location"),
        ("Host", "host"),
        ("Cleanliness", "clean"),
    ]
    theme = next((name for name, keyword in themes if keyword in text), "General")
    return sentiment, theme


def json_error(message, status=400, details=None):
    payload = {"success": False, "error": message}
    if details:
        payload["details"] = details
    return jsonify(payload), status


@jwt.token_in_blocklist_loader
def check_if_token_revoked(jwt_header, jwt_payload):
    conn = get_db()
    row = conn.execute("SELECT 1 FROM revoked_tokens WHERE jti = ?", (jwt_payload["jti"],)).fetchone()
    conn.close()
    return row is not None


@jwt.expired_token_loader
def expired_token(jwt_header, jwt_payload):
    return json_error("Token has expired. Please log in again.", 401)


@jwt.invalid_token_loader
def invalid_token(error):
    return json_error("Invalid authentication token.", 401)


@jwt.unauthorized_loader
def missing_token(error):
    return json_error("Authorization token is required.", 401)


@app.errorhandler(429)
def rate_limit_error(error):
    return json_error("Too many requests. Please try again later.", 429)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/login")
def login_page():
    return render_template("login.html")


@app.route("/register")
def register_page():
    return render_template("register.html")


@app.route("/dashboard")
def dashboard_page():
    return render_template("dashboard.html")


@app.route("/analysis")
def analysis_page():
    return render_template("analysis.html")


@app.post("/api/auth/register")
@limiter.limit("5 per minute")
def register():
    data = request.get_json(silent=True) or {}
    email = data.get("email", "").strip().lower()
    password = data.get("password", "")
    errors = validate_credentials(email, password)
    if errors:
        return json_error("Validation failed.", 400, errors)

    password_hash = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt(rounds=12))
    conn = get_db()
    try:
        cursor = conn.execute(
            "INSERT INTO users (email, password_hash) VALUES (?, ?)",
            (email, password_hash),
        )
        conn.commit()
    except sqlite3.IntegrityError:
        conn.close()
        return json_error("Email is already registered.", 400)
    conn.close()

    return jsonify({
        "success": True,
        "message": "Registration successful.",
        "user": {"id": cursor.lastrowid, "email": email},
    }), 201


@app.post("/api/auth/login")
@limiter.limit("5 per minute")
def login():
    data = request.get_json(silent=True) or {}
    email = data.get("email", "").strip().lower()
    password = data.get("password", "")
    errors = validate_credentials(email, password)
    if errors:
        return json_error("Validation failed.", 400, errors)

    conn = get_db()
    user = conn.execute("SELECT id, email, password_hash FROM users WHERE email = ?", (email,)).fetchone()
    conn.close()

    if not user or not bcrypt.checkpw(password.encode("utf-8"), user["password_hash"]):
        return json_error("Invalid email or password.", 401)

    token = create_access_token(identity=str(user["id"]), additional_claims={"email": user["email"]})
    return jsonify({
        "success": True,
        "message": "Login successful.",
        "access_token": token,
        "token_type": "Bearer",
        "expires_in_days": 7,
        "user": {"id": user["id"], "email": user["email"]},
    })


@app.post("/api/auth/logout")
@jwt_required()
def logout():
    jti = get_jwt()["jti"]
    conn = get_db()
    conn.execute("INSERT OR IGNORE INTO revoked_tokens (jti) VALUES (?)", (jti,))
    conn.commit()
    conn.close()
    return jsonify({"success": True, "message": "Logged out successfully."})


@app.get("/api/auth/me")
@jwt_required()
def me():
    user_id = int(get_jwt_identity())
    conn = get_db()
    user = conn.execute("SELECT id, email, created_at FROM users WHERE id = ?", (user_id,)).fetchone()
    conn.close()
    if not user:
        return json_error("User not found.", 404)
    return jsonify({"success": True, "user": dict(user)})


@app.get("/api/reviews")
@jwt_required()
def list_reviews():
    user_id = int(get_jwt_identity())
    conn = get_db()
    rows = conn.execute("SELECT * FROM reviews WHERE user_id = ? ORDER BY id DESC", (user_id,)).fetchall()
    conn.close()
    return jsonify({"success": True, "count": len(rows), "reviews": [dict(row) for row in rows]})


@app.get("/api/reviews/<int:review_id>")
@jwt_required()
def get_review(review_id):
    user_id = int(get_jwt_identity())
    conn = get_db()
    row = conn.execute("SELECT * FROM reviews WHERE id = ? AND user_id = ?", (review_id, user_id)).fetchone()
    conn.close()
    if not row:
        return json_error("Review not found.", 404)
    return jsonify({"success": True, "review": dict(row)})


@app.post("/api/reviews")
@jwt_required()
def create_review():
    data = request.get_json(silent=True) or {}
    review = str(data.get("review", "")).strip()
    if not review:
        return json_error("Review text is required.", 400)
    if len(review) > 2000:
        return json_error("Review must be 2000 characters or fewer.", 400)

    sentiment, theme = analyze_review(review)
    user_id = int(get_jwt_identity())
    conn = get_db()
    cursor = conn.execute(
        "INSERT INTO reviews (user_id, review, sentiment, theme) VALUES (?, ?, ?, ?)",
        (user_id, review, sentiment, theme),
    )
    conn.commit()
    row = conn.execute("SELECT * FROM reviews WHERE id = ?", (cursor.lastrowid,)).fetchone()
    conn.close()
    return jsonify({"success": True, "message": "Review created.", "review": dict(row)}), 201


@app.put("/api/reviews/<int:review_id>")
@app.patch("/api/reviews/<int:review_id>")
@jwt_required()
def update_review(review_id):
    data = request.get_json(silent=True) or {}
    review = str(data.get("review", "")).strip()
    if not review:
        return json_error("Review text is required.", 400)

    sentiment, theme = analyze_review(review)
    user_id = int(get_jwt_identity())
    conn = get_db()
    cursor = conn.execute(
        "UPDATE reviews SET review = ?, sentiment = ?, theme = ? WHERE id = ? AND user_id = ?",
        (review, sentiment, theme, review_id, user_id),
    )
    conn.commit()
    row = conn.execute("SELECT * FROM reviews WHERE id = ? AND user_id = ?", (review_id, user_id)).fetchone()
    conn.close()
    if cursor.rowcount == 0:
        return json_error("Review not found.", 404)
    return jsonify({"success": True, "message": "Review updated.", "review": dict(row)})


@app.delete("/api/reviews/<int:review_id>")
@jwt_required()
def delete_review(review_id):
    user_id = int(get_jwt_identity())
    conn = get_db()
    cursor = conn.execute("DELETE FROM reviews WHERE id = ? AND user_id = ?", (review_id, user_id))
    conn.commit()
    conn.close()
    if cursor.rowcount == 0:
        return json_error("Review not found.", 404)
    return jsonify({"success": True, "message": "Review deleted."})


@app.get("/api/reviews/search")
@jwt_required()
def search_reviews():
    q = request.args.get("q", "").strip()
    user_id = int(get_jwt_identity())
    conn = get_db()
    rows = conn.execute(
        "SELECT * FROM reviews WHERE user_id = ? AND (review LIKE ? OR theme LIKE ? OR sentiment LIKE ?) ORDER BY id DESC",
        (user_id, f"%{q}%", f"%{q}%", f"%{q}%"),
    ).fetchall()
    conn.close()
    return jsonify({"success": True, "query": q, "count": len(rows), "reviews": [dict(row) for row in rows]})


# ---------- OAuth ----------
@app.get("/auth/google")
def google_login():
    if "google" not in oauth._clients:
        return json_error("Google OAuth is not configured. Add GOOGLE_CLIENT_ID and GOOGLE_CLIENT_SECRET to .env.", 503)
    redirect_uri = url_for("google_callback", _external=True)
    return oauth.google.authorize_redirect(redirect_uri)


@app.get("/auth/google/callback")
def google_callback():
    if "google" not in oauth._clients:
        return json_error("Google OAuth is not configured.", 503)
    token = oauth.google.authorize_access_token()
    userinfo = token.get("userinfo")
    if not userinfo:
        userinfo = oauth.google.get("https://openidconnect.googleapis.com/v1/userinfo").json()
    return oauth_user_login(userinfo.get("email"))


@app.get("/auth/github")
def github_login():
    if "github" not in oauth._clients:
        return json_error("GitHub OAuth is not configured. Add GITHUB_CLIENT_ID and GITHUB_CLIENT_SECRET to .env.", 503)
    redirect_uri = url_for("github_callback", _external=True)
    return oauth.github.authorize_redirect(redirect_uri)


@app.get("/auth/github/callback")
def github_callback():
    if "github" not in oauth._clients:
        return json_error("GitHub OAuth is not configured.", 503)
    token = oauth.github.authorize_access_token()
    profile = oauth.github.get("user").json()
    email = profile.get("email")
    if not email:
        emails = oauth.github.get("user/emails").json()
        email = next((item["email"] for item in emails if item.get("primary") and item.get("verified")), None)
    return oauth_user_login(email)


def oauth_user_login(email):
    if not email:
        return json_error("OAuth provider did not return a verified email address.", 400)
    email = email.lower().strip()
    conn = get_db()
    user = conn.execute("SELECT id, email FROM users WHERE email = ?", (email,)).fetchone()
    if not user:
        random_password = bcrypt.hashpw(os.urandom(32), bcrypt.gensalt(rounds=12))
        cursor = conn.execute("INSERT INTO users (email, password_hash) VALUES (?, ?)", (email, random_password))
        conn.commit()
        user_id = cursor.lastrowid
    else:
        user_id = user["id"]
    conn.close()
    token = create_access_token(identity=str(user_id), additional_claims={"email": email})
    # The frontend reads the token from this query parameter and immediately moves it into localStorage.
    return redirect(url_for("oauth_complete", token=token))


@app.get("/oauth-complete")
def oauth_complete():
    return render_template("oauth_complete.html")


if __name__ == "__main__":
    init_db()
    app.run(debug=True)
