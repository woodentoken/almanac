import os
import sqlite3
from datetime import datetime
from livereload import Server
from dotenv import load_dotenv

from flask import Flask, flash, redirect, render_template, request, url_for, abort
import markdown
from werkzeug.utils import secure_filename
BLOG_DIR = 'posts'


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

@app.route('/blog')
def blog_index():
    # List all .md files and extract slugs
    posts = []
    for filename in os.listdir(BLOG_DIR):
        if filename.endswith('.md'):
            slug = filename[:-3]  # Remove ".md"
            title = slug.replace('-', ' ').title()
            posts.append({'slug': slug, 'title': title})
    
    return render_template('blog_index.html', posts=posts)

@app.route('/blog/<slug>')
def blog_post(slug):
    md_path = os.path.join(BLOG_DIR, f'{slug}.md')
    if not os.path.exists(md_path):
        abort(404)

    with open(md_path, 'r', encoding='utf-8') as f:
        md_content = f.read()
        html = markdown.markdown(md_content, extensions=['fenced_code', 'codehilite'])

    return render_template('post.html', content=html, title=slug.replace("-", " ").title())


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
