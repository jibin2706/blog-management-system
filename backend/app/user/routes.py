from flask import request, Blueprint, jsonify, abort
from app.models import Post, User
from app.auth.func import requires_auth

user = Blueprint('user', __name__)


@user.route('/featured')
def get_featured_posts():
    result = Post.query.filter(Post.is_featured == True).all()

    posts = [post.format() for post in result]
    return jsonify({
        'sucesss': True,
        'posts': posts
    })


@user.route('/post')
def get_post():
    post_slug = request.args.get('url', None)

    if post_slug is None:
        return abort(400)

    result = Post.query.filter(Post.url_slug == post_slug).first()

    if result is None:
        return abort(404)

    post = result.format()
    writer = result.user.format()
    return jsonify({
        'sucesss': True,
        'post': post,
        'writer': writer
    })


@user.route('/post', methods=['POST'])
@requires_auth()
def save_post(user):
    body = request.get_json()

    try:
        new_post = Post(user_id=user.id, title=body['title'],
                        url_slug=body['url_slug'],
                        body=body['body'], is_publish=body['is_publish'])
        new_post.insert()
    except Exception as e:
        print(e)
        return abort(404)

    return jsonify({
        'sucesss': True
    })
