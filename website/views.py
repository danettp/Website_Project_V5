from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify
from flask_login import login_required, current_user
from .models import Post, User, Comment, Like
from . import db

# Create a Blueprint for the views
views = Blueprint("views", __name__)

# Route for the home page
@views.route("/")
@views.route("/home")
def home():
    # Query all posts from the database
    posts = Post.query.all()
    return render_template("home.html", user=current_user, posts=posts)

@views.route("/blog")
@login_required
def blog():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.date_created.desc()).paginate(page=page, per_page=4)
    return render_template("blog.html", user=current_user, posts=posts)

@views.route("/create-post", methods=['GET', 'POST'])
@login_required
def create_post():
    if request.method == "POST":
        text = request.form.get('text')

        if not text:
            flash('Post cannot be empty', category='error')
        else:
            post = Post(text=text, author=current_user.id)
            db.session.add(post)
            db.session.commit()
            flash('Post created!', category='success')
            return redirect(url_for('views.blog'))

    return render_template('create_post.html', user=current_user)

# Route for deleting a post
@views.route("/delete-post/<id>")
@login_required
def delete_post(id):
    post = Post.query.filter_by(id=id).first() # Find the post by its ID

    if not post:
        flash("Post does not exist.", category='error')
    elif current_user.id != post.id:
        flash('You do not have permission to delete this post.', category='error')
    else:
        # Delete the post from the database
        db.session.delete(post)
        db.session.commit()
        flash('Post deleted.', category='success')

    return redirect(url_for('views.blog'))

# Route for displaying all posts by a specific user
@views.route("/posts/<username>")
@login_required
def posts(username):
    user = User.query.filter_by(username=username).first() # Find the user by their username

    if not user:
        flash('No user with that username exists.', category='error')
        return redirect(url_for('views.blog'))

    posts = user.posts # Get all posts by the user
    return render_template("posts.html", user=current_user, posts=posts, username=username)

# Route for creating a new comment on a post
@views.route("/create-comment/<post_id>", methods=['POST'])
@login_required
def create_comment(post_id):
    text = request.form.get('text')

    if not text:
        flash('Comment cannot be empty.', category='error')
    else:
        post = Post.query.filter_by(id=post_id) # Find the post by its ID
        if post:
            # Create a new comment and add it to the database
            comment = Comment(
                text=text, author=current_user.id, post_id=post_id)
            db.session.add(comment)
            db.session.commit()
        else:
            flash('Post does not exist.', category='error')

    return redirect(url_for('views.blog'))

# Route for deleting a comment
@views.route("/delete-comment/<comment_id>")
@login_required
def delete_comment(comment_id):
    comment = Comment.query.filter_by(id=comment_id).first()

    if not comment:
        flash('Comment does not exist.', category='error')
    elif current_user.id != comment.author and current_user.id != comment.post.author:
        flash('You do not have permission to delete this comment.', category='error')
    else:
        db.session.delete(comment) # Delete the comment from the database
        db.session.commit()

    return redirect(url_for('views.blog'))

# Route for liking a post
@views.route("/like-post/<post_id>", methods=['POST'])
@login_required
def like(post_id):
    post = Post.query.filter_by(id=post_id).first()
    like = Like.query.filter_by(
        author=current_user.id, post_id=post_id).first() # Check if the user has already liked the post

    if not post:
        return jsonify({'error': 'Post does not exist.'}, 400)
    elif like:
        # If the user has already liked the post, remove the like
        db.session.delete(like)
        db.session.commit()
    else:
        # If the user hasn't liked the post, add a new like
        like = Like(author=current_user.id, post_id=post_id)
        db.session.add(like)
        db.session.commit()

    return jsonify({"likes": len(post.likes), "liked": current_user.id in map(lambda x: x.author, post.likes)}) 