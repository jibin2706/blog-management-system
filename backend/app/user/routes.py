from flask import request, Blueprint, jsonify, abort
from app.models import Post, User
from app.auth.func import requires_auth
from sqlalchemy import and_

user = Blueprint('user', __name__)


'''
Query Parameter
     type -> enum (featured, latest)
        featured - returns featured posts containing Post.is_featured = True
        latest - returns posts by sorted Post.created_at
    limit -> int
        default value = 10
'''
@user.route('/posts')
def get_posts():
    postType = request.args.get('type', 'latest', str)
    limit = request.args.get('limit', 10, int)

    result = []
    if postType == 'featured':
        result = Post.query.filter(
            and_(Post.is_featured == True, Post.is_publish == True)).limit(limit).all()
    elif postType == 'latest':
        result = Post.query.filter(Post.is_publish == True).order_by(
            Post.created_at.desc()).limit(limit).all()

    posts = [post.format_short() for post in result]
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
