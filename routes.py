# from flask import render_template, request, redirect, url_for
# from .post import Post, db
# # ...existing code...

# @app.route('/edit_post/<int:post_id>', methods=['GET', 'POST'])
# def edit_post(post_id):
#     post = Post.query.get_or_404(post_id)
#     if request.method == 'POST':
#         post.title = request.form['title']
#         post.description = request.form['description']
#         db.session.commit()
#         return redirect(url_for('view_post', post_id=post.id))
#     return render_template('edit_post.html', post=post)

# @app.route('/view_post/<int:post_id>')
# def view_post(post_id):
#     post = Post.query.get_or_404(post_id)
#     photos = Photo.query.filter_by(post_id=post_id).all()
#     return render_template('view_post.html', post=post, photos=photos)

# # ...existing code...
