from flask import Flask, render_template, request, redirect, url_for, flash
from werkzeug.utils import secure_filename
from datetime import datetime
import os
import sqlite3

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here'
app.config['UPLOAD_FOLDER'] = 'static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def init_db():
    conn = sqlite3.connect('photoblog.db')
    c = conn.cursor()
    # Create posts table
    c.execute('''
        CREATE TABLE IF NOT EXISTS posts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    # Create photos table with foreign key to posts
    c.execute('''
        CREATE TABLE IF NOT EXISTS photos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            post_id INTEGER NOT NULL,
            image_path TEXT NOT NULL,
            caption TEXT,
            position INTEGER,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (post_id) REFERENCES posts (id)
        )
    ''')
    conn.commit()
    conn.close()

def get_db():
    conn = sqlite3.connect('photoblog.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    db = get_db()
    posts = db.execute('''
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
    ''').fetchall()
    db.close()
    return render_template('index.html', posts=posts)

@app.route('/post/<int:post_id>')
def view_post(post_id):
    db = get_db()
    post = db.execute('SELECT * FROM posts WHERE id = ?', [post_id]).fetchone()
    photos = db.execute('SELECT * FROM photos WHERE post_id = ?', [post_id]).fetchall()
    db.close()
    return render_template('view_post.html', post=post, photos=photos)

@app.route('/post/new', methods=['GET', 'POST'])
def new_post():
    if request.method == 'POST':
        if 'photos' not in request.files:
            flash('No files selected')
            return redirect(request.url)
        
        files = request.files.getlist('photos')
        if not files or files[0].filename == '':
            flash('No files selected')
            return redirect(request.url)
        
        db = get_db()
        cursor = db.execute('INSERT INTO posts (title, description) VALUES (?, ?)',
                          [request.form['title'], request.form['description']])
        post_id = cursor.lastrowid
        
        for index, file in enumerate(files):
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S_')
                filename = timestamp + filename
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                
                caption = request.form.get('caption', '') or ''
                
                db.execute('INSERT INTO photos (post_id, image_path, caption, position) VALUES (?, ?, ?, ?)',
                        [post_id, filename, caption, index])
        
        db.commit()
        db.close()
        
        flash('Post created successfully!')
        return redirect(url_for('view_post', post_id=post_id))
            
    return render_template('new_post.html')

@app.route('/post/edit/<int:post_id>', methods=['GET', 'POST'])
def edit_post(post_id):
    db = get_db()
    post = db.execute('SELECT * FROM posts WHERE id = ?', [post_id]).fetchone()
    photos = db.execute('SELECT * FROM photos WHERE post_id = ?', [post_id]).fetchall()
    
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        
        db.execute('UPDATE posts SET title = ?, description = ? WHERE id = ?', [title, description, post_id])
        
        if 'photos' in request.files:
            files = request.files.getlist('photos')
            for index, file in enumerate(files):
                if file and allowed_file(file.filename):
                    filename = secure_filename(file.filename)
                    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S_')
                    filename = timestamp + filename
                    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                    
                    caption = request.form.get('caption', '') or ''
                    
                    db.execute('INSERT INTO photos (post_id, image_path, caption, position) VALUES (?, ?, ?, ?)', [post_id, filename, caption, index])
        
        db.commit()
        db.close()
        
        flash('Post updated successfully!')
        return redirect(url_for('view_post', post_id=post_id))
    
    db.close()
    return render_template('edit_post.html', post=post, photos=photos)

if __name__ == '__main__':
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    init_db()
    app.run(debug=True)