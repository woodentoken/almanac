import os
import sqlite3
from datetime import datetime
from paragraph import Paragraph
from post import Post
from livereload import Server
from dotenv import load_dotenv

from flask import Flask, flash, redirect, render_template, request, url_for
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config["SECRET_KEY"] = "your-secret-key-here"
app.config["UPLOAD_FOLDER"] = "static/uploads"
load_dotenv()

# Always enable Jinja auto-reload in development
if os.environ.get("FLASK_ENV") == "development":
    print("loaded .env - running in development mode with live reload enabled.")
    app.config["TEMPLATES_AUTO_RELOAD"] = True
    app.jinja_env.auto_reload = True
    USE_LIVERELOAD = True
else:
    USE_LIVERELOAD = False

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
