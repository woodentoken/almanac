import sqlite3

class Paragraph:
    def __init__(self, id, post_id, content, position, created_at):
        self.id = id
        self.post_id = post_id
        self.content = content
        self.position = position
        self.created_at = created_at

    @staticmethod
    def get_by_post_id(post_id):
        conn = sqlite3.connect("photoblog.db")
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM paragraphs WHERE post_id = ?", (post_id,))
        rows = cursor.fetchall()
        conn.close()
        return [Paragraph(**row) for row in rows]

    @staticmethod
    def update(paragraph_id, content):
        conn = sqlite3.connect("photoblog.db")
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE paragraphs SET content = ? WHERE id = ?",
            (content, paragraph_id)
        )
        conn.commit()
        conn.close()
        
    @staticmethod
    def delete(paragraph_id):
        conn = sqlite3.connect("photoblog.db")
        cursor = conn.cursor()
        cursor.execute("DELETE FROM paragraphs WHERE id = ?", (paragraph_id,))
        conn.commit()
        conn.close()
