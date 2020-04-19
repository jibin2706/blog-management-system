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
@requires_auth('post:article')
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


@user.route('/post', methods=['PATCH'])
@requires_auth('patch:article')
def update_post(user):
    body = request.get_json()

    post = Post.query.filter(Post.id == body['id']).first()
    if post is None:
        return abort(404)

    try:
        post.title = body['title']
        post.url_slug = body['url_slug']
        post.body = body['body']
        post.is_publish = body['is_publish']
        post.update()
    except Exception as e:
        print(e)
        return abort(404)

    return jsonify({
        'sucesss': True
    })


@user.route('/post/<post_id>', methods=['DELETE'])
@requires_auth('delete:article')
def delete_post(user, post_id):
    body = request.get_json()

    post = Post.query.filter(Post.id == post_id).first()
    if post is None:
        return abort(404)

    try:
        post.delete()
    except Exception as e:
        print(e)
        return abort(401)

    return jsonify({
        'sucesss': True
    })


# Error handlers
@user.app_errorhandler(400)
def page_not_found(e):
    return jsonify({
        'success': False,
        'message': 'Bad Request'
    }), 400


@user.app_errorhandler(401)
def page_not_found(e):
    return jsonify({
        'success': False,
        'message': 'Not Authorized to make this request'
    }), 405


@user.app_errorhandler(404)
def page_not_found(e):
    return jsonify({
        'success': False,
        'message': 'Page not found'
    }), 404


@user.app_errorhandler(405)
def page_not_found(e):
    return jsonify({
        'success': False,
        'message': 'Method not allowed'
    }), 405


@user.app_errorhandler(422)
def page_not_found(e):
    return jsonify({
        'success': False,
        'message': 'Request cannot be processed'
    }), 422
