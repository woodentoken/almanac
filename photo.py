import sqlite3

class Photo:
    def __init__(self, id, post_id, image_path, caption, position, created_at):
        self.id = id
        self.post_id = post_id
        self.image_path = image_path
        self.caption = caption
        self.position = position
        self.created_at = created_at

    @staticmethod
    def get_by_post_id(post_id):
        conn = sqlite3.connect("photoblog.db")
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM photos WHERE post_id = ?", (post_id,))
        rows = cursor.fetchall()
        conn.close()
        return [Photo(**row) for row in rows]
