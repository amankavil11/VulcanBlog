from flask import render_template, Blueprint, request
from flaskBlog.models import user, post

main = Blueprint('Main', __name__)


@main.route("/")
@main.route("/home")
def Home():
    #posts = post.query.all()
    #posts = post.query.order_by(post.id.desc())
    page = request.args.get('page', 1, type=int)
    posts = post.query.order_by(post.date_posted.desc()).paginate(per_page=10, page=page)
    return render_template('home.html', post=posts)


@main.route("/about")
def About():
    return render_template('about.html', title="About")