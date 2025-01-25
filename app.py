import os
import sqlite3
from datetime import datetime
from paragraph import Paragraph
from photo import Photo
from post import Post

from flask import Flask, flash, redirect, render_template, request, url_for
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config["SECRET_KEY"] = "your-secret-key-here"
app.config["UPLOAD_FOLDER"] = "static/uploads"
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif"}


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


def init_db():
    conn = sqlite3.connect("photoblog.db")
    c = conn.cursor()
    # Create posts table
    c.execute("""
        CREATE TABLE IF NOT EXISTS posts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    # Create photos table with foreign key to posts
    c.execute("""
        CREATE TABLE IF NOT EXISTS photos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            post_id INTEGER NOT NULL,
            image_path TEXT NOT NULL,
            caption TEXT,
            position INTEGER,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (post_id) REFERENCES posts (id)
        )
    """)
    # create paragraph table with foreign key to posts
    c.execute("""
        CREATE TABLE IF NOT EXISTS paragraphs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            post_id INTEGER NOT NULL,
            content TEXT NOT NULL,
            position INTEGER,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (post_id) REFERENCES posts (id)
        )
    """)
    conn.commit()
    conn.close()


def get_db():
    conn = sqlite3.connect("photoblog.db")
    conn.row_factory = sqlite3.Row
    return conn

@app.route("/")
def splash():
    return render_template("splash.html")

@app.route("/series")
def series():
    return render_template("series.html")

@app.route("/portfolio")
def portfolio():
    return render_template("portfolio.html")

@app.route("/contact")
def contact():
    return render_template("contact.html")

@app.route("/blog")
def blog():
    db = get_db()
    posts = db.execute("""
        SELECT p.id, 
               p.title, 
               p.description, 
               datetime(p.created_at) as created_at,
               ph.image_path as cover_image,
               (SELECT COUNT(*) FROM photos WHERE post_id = p.id) as photo_count
        FROM posts p
        LEFT JOIN photos ph ON p.id = ph.post_id
        GROUP BY p.id
        ORDER BY p.created_at DESC
    """).fetchall()
    db.close()
    return render_template("blog.html", posts=posts)

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/post/<int:post_id>", methods=["GET", "POST"])
def view_post(post_id):
    db = get_db()
    post = db.execute("SELECT * FROM posts WHERE id = ?", [post_id]).fetchone()
    photos = db.execute("SELECT * FROM photos WHERE post_id = ?", [post_id]).fetchall()
    paragraphs = db.execute("SELECT * FROM paragraphs WHERE post_id = ?", [post_id]).fetchall()

    if request.method == "POST":
        if "content" in request.form:
            content = request.form["content"]
            position = len(paragraphs) + 1
            db.execute(
                "INSERT INTO paragraphs (post_id, content, position) VALUES (?, ?, ?)",
                [post_id, content, position]
            )
            flash("Paragraph added successfully!")
        elif "photo" in request.files:
            file = request.files["photo"]
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_")
                filename = timestamp + filename
                file.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))

                caption = request.form.get("caption", "") or ""
                position = len(photos) + 1

                db.execute(
                    "INSERT INTO photos (post_id, image_path, caption, position) VALUES (?, ?, ?, ?)",
                    [post_id, filename, caption, position]
                )
                flash("Photo added successfully!")
        db.commit()
        db.close()
        return redirect(url_for("view_post", post_id=post_id))

    db.close()
    return render_template("view_post.html", post=post, photos=photos, paragraphs=paragraphs)

@app.route("/paragraph/<int:post_id><int:paragraph_id>/edit", methods=["POST"])
def edit_paragraph(post_id, paragraph_id):
    Paragraph.update(paragraph_id, request.form["content"])
    flash(f"Paragraph of post {post_id} updated successfully.")
    return redirect(request.referrer)

@app.route("/paragraph/<int:post_id><int:paragraph_id>/delete", methods=["POST"])
def delete_paragraph(post_id, paragraph_id):
    Paragraph.delete(paragraph_id)
    flash(f"Paragraph of post {post_id} deleted successfully.")
    return redirect(request.referrer)

@app.route("/post/new", methods=["GET", "POST"])
def new_post():
    
    if request.method == "POST":
        db = get_db()
        cursor = db.execute(
            "INSERT INTO posts (title, description) VALUES (?, ?)",
            [request.form["title"], request.form["description"]],
        )
        post_id = cursor.lastrowid

        db.commit()
        db.close()

        flash("Post created successfully!")
        return redirect(url_for("view_post", post_id=post_id))

    return render_template("new_post.html")

@app.route("/post/<int:post_id>/delete", methods=["POST"])
def delete_post(post_id):
    Post.delete(post_id)
    flash("Post and all associated photos and paragraphs deleted successfully!")
    return redirect(url_for("index"))

if __name__ == "__main__":
    os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)
    init_db()
    app.run(debug=True)
