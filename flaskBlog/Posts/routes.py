from flask import Blueprint
from flaskBlog import db
from flask_login import current_user, login_required
from flask import render_template, url_for, flash, redirect, request, abort
from flaskBlog.Posts.forms import *
from flaskBlog.models import post

posts = Blueprint('Posts', __name__)


@posts.route("/post/new", methods=['GET', 'POST'])
@login_required
def New_Post():
    form = PostForm()
    if form.validate_on_submit():
        Post = post(title=form.title.data, content=form.content.data, author=current_user)
        db.session.add(Post)
        db.session.commit()
        flash('Post has been created', 'success')
        return redirect((url_for('Main.Home')))
    return render_template('create_post.html', title='New Post', form=form, legend='New Post')


@posts.route("/post/<int:post_id>")
def IndividualPost(post_id):
    Post = post.query.get_or_404(post_id)
    return render_template('post.html', title=Post.title, post=Post)


@posts.route("/post/<int:post_id>/edit", methods=['GET', 'POST'])
@login_required
def Edit_Post(post_id):
    Post = post.query.get_or_404(post_id)
    if Post.author != current_user:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        Post.title = form.title.data
        Post.content = form.content.data
        db.session.commit()
        flash('Your post has been updated!', 'success')
        return redirect(url_for('Posts.IndividualPost', post_id=Post.id))
    elif request.method == 'GET':
        form.title.data = Post.title
        form.content.data = Post.content
    
    return render_template('create_post.html', title='Edit Post', form=form, legend='Edit Post')


@posts.route("/post/<int:post_id>/delete", methods=['GET', 'POST'])
@login_required
def Delete_Post(post_id):
    Post = post.query.get_or_404(post_id)
    if Post.author != current_user:
        abort(403)
    db.session.delete(Post)
    db.session.commit()
    flash('Your post has been deleted!', 'success')
    return redirect(url_for('Main.Home'))
