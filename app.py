import os
import psycopg2
from datetime import datetime
from dotenv import load_dotenv

from flask import (
    Flask,
    flash,
    redirect,
    render_template,
    request,
    url_for,
    abort,
    send_from_directory,
    make_response,
)
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail, Message
import markdown
from werkzeug.utils import secure_filename

BLOG_DIR = "posts"

app = Flask(__name__)

load_dotenv()  # This loads variables from .env in dev only

app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "fallback-dev-secret")
app.config["UPLOAD_FOLDER"] = "static/uploads"

# Always enable Jinja auto-reload in development
if os.environ.get("FLASK_ENV") == "development":
    print("loaded .env - running in development mode with live reload enabled.")
    app.config["TEMPLATES_AUTO_RELOAD"] = True
    app.jinja_env.auto_reload = True
    USE_LIVERELOAD = True
else:
    USE_LIVERELOAD = False


# database_url = os.environ.get("DATABASE_URL")
# if not database_url:
#     database_url = "sqlite:///emails.db"  # Fallback to SQLite for local dev
#     print("using local database file")
#     app.config["SQLALCHEMY_DATABASE_URI"] = database_url

# if database_url.startswith("postgres://"):
#     database_url = database_url.replace("postgres://", "postgresql://", 1)
#     app.config["SQLALCHEMY_DATABASE_URI"] = database_url

# app.config["SQLALCHEMY_DATABASE_URI"] = database_url
# app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# db = SQLAlchemy(app)


# Define Email model
# class Email(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     address = db.Column(db.String(120), unique=True, nullable=False)


# with app.app_context():
#     db.create_all()  # Create tables if they don't exist


# @app.route("/subscribe", methods=["POST"])
# def subscribe():
#     email_input = request.form.get("email")
#     if email_input:
#         new_email = Email(address=email_input)
#         try:
#             db.session.add(new_email)
#             db.session.commit()
#         except:
#             db.session.rollback()
#     return redirect("/contact")  # send them back to homepage (or any page you like)


# --- Static file caching ---
@app.route("/static/<path:filename>")
def static_files(filename):
    response = make_response(send_from_directory("static", filename))
    print(f"Serving static file: {filename}")
    # Cache for 1 year
    response.headers["Cache-Control"] = "public, max-age=31536000, immutable"
    return response


# --- Routes ---
@app.route("/")
def splash():
    return render_template("splash.html")


@app.route("/series")
def series():
    return render_template("series.html")


@app.route("/series/japan")
def series_japan():
    return render_template("series_japan.html")


@app.route("/series/westing")
def series_westing():
    return render_template("series_westing.html")


@app.route("/portfolio")
def portfolio():
    return render_template("portfolio.html")


@app.route("/contact")
def contact():
    return render_template("contact.html")


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/blog")
def blog_index():
    # List all .md files and extract slugs
    posts = []
    for filename in os.listdir(BLOG_DIR):
        if filename.endswith(".md"):
            slug = filename[:-3]  # Remove ".md"
            title = slug.replace("-", " ").title()
            posts.append({"slug": slug, "title": title})

    return render_template("blog_index.html", posts=posts)


@app.route("/blog/<slug>")
def blog_post(slug):
    md_path = os.path.join(BLOG_DIR, f"{slug}.md")
    if not os.path.exists(md_path):
        abort(404)

    with open(md_path, "r", encoding="utf-8") as f:
        md_content = f.read()
        html = markdown.markdown(md_content, extensions=["fenced_code", "codehilite"])

    return render_template(
        "post.html", content=html, title=slug.replace("-", " ").title()
    )


# --- Run server ---
if __name__ == "__main__":
    if USE_LIVERELOAD:
        from livereload import Server

        server = Server(app.wsgi_app)
        server.watch("templates/**/*.html")
        server.watch("static/css/**/*.css")
        server.watch("static/js/**/*.js")
        server.serve(port=5500)
    else:
        app.run(host="0.0.0.0", port=8000)  # Or use gunicorn in production
