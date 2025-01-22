import sqlite3
from paragraph import Paragraph
from photo import Photo
import datetime

class Post:
    def __init__(self, id, title, description, created_at):
        self.id = id
        self.title = title
        self.description = description
        self.created_at = created_at
        self.paragraphs = Paragraph.get_by_post_id(id)
        self.photos = Photo.get_by_post_id(id)

    @staticmethod
    def get_all():
        conn = sqlite3.connect("photoblog.db")
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM posts ORDER BY created_at DESC")
        rows = cursor.fetchall()
        conn.close()
        return [Post(**row) for row in rows]

    @staticmethod
    def get_by_id(post_id):
        conn = sqlite3.connect("photoblog.db")
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM posts WHERE id = ?", (post_id,))
        row = cursor.fetchone()
        conn.close()
        if row:
            return Post(**row)
        return None

    @staticmethod
    def create(title, description):
        conn = sqlite3.connect("photoblog.db")
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO posts (title, description) VALUES (?, ?)",
            (title, description)
        )
        conn.commit()
        post_id = cursor.lastrowid
        conn.close()
        return post_id

    @staticmethod
    def update(post_id, title, description):
        conn = sqlite3.connect("photoblog.db")
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE posts SET title = ?, description = ? WHERE id = ?",
            (title, description, post_id)
        )
        conn.commit()
        conn.close()

    @staticmethod
    def delete(post_id):
        conn = sqlite3.connect("photoblog.db")
        cursor = conn.cursor()
        cursor.execute("DELETE FROM paragraphs WHERE post_id = ?", (post_id,))
        cursor.execute("DELETE FROM photos WHERE post_id = ?", (post_id,))
        cursor.execute("DELETE FROM posts WHERE id = ?", (post_id,))
        conn.commit()
        conn.close()

    @staticmethod
    def update_paragraph(paragraph_id, content):
        conn = sqlite3.connect("photoblog.db")
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE paragraphs SET content = ? WHERE id = ?",
            (content, paragraph_id)
        )
        conn.commit()
        conn.close()

    @staticmethod
    def delete_paragraph(paragraph_id):
        conn = sqlite3.connect("photoblog.db")
        cursor = conn.cursor()
        cursor.execute("DELETE FROM paragraphs WHERE id = ?", (paragraph_id,))
        conn.commit()
        conn.close()
