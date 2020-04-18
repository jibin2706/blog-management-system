from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from sqlalchemy import Column, Boolean, String, Integer, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import JSONB
from .settings import DATABASE, HOST, DB_PASSWORD, DB_USER, DB_NAME


db = SQLAlchemy()


def setup_db(app):
    app.config['SQLALCHEMY_DATABASE_URI'] = f'{DATABASE}://{DB_USER}:{DB_PASSWORD}@{HOST}/{DB_NAME}'
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    migrate = Migrate(app, db)
    db.init_app(app)


class User(db.Model):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    email = Column(String(150), nullable=False)
    picture = Column(String)
    bio = Column(String, default='')
    role = Column(String, default='writer')
    posts = relationship('Post', backref='user',
                         cascade='all, delete-orphan')

    def __init__(self, name, email, picture=None, bio=None):
        self.name = name
        self.email = email
        self.picture = picture
        self.bio = bio

    def __repr__(self):
        return f'<User id:{self.id} name:{self.name}>'

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def format(self):
        return {
            'name': self.name,
            'email': self.email,
            'picture': self.picture,
            'bio': self.bio,
            'role': self.role
        }


class Post(db.Model):
    __tablename__ = 'posts'

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String, nullable=False)
    url_slug = Column(String, nullable=False, primary_key=True)
    body = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.now())
    updated_at = Column(DateTime, default=datetime.now())
    is_publish = Column(Boolean, default=False)
    is_featured = Column(Boolean, default=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)

    def __init__(self, title, body, url_slug, user_id, is_publish=None):
        self.title = title
        self.body = body
        self.url_slug = url_slug
        self.is_publish = is_publish
        self.user_id = user_id

    def __repr__(self):
        return f'<Post id:{self.id} url:{self.url_slug} user_id:{self.user_id}>'

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def format_short(self):
        return {
            'id': self.id,
            'title': self.title,
            'body': self.body[:150],
            'url_slug': self.url_slug,
            'created_at': self.created_at.strftime('%b %d, %Y'),
            'updated_at': self.updated_at,
            'is_publish': self.is_publish,
            'is_featured': self.is_featured,
            'user_id': self.user_id
        }

    def format(self):
        return {
            'id': self.id,
            'title': self.title,
            'body': self.body,
            'url_slug': self.url_slug,
            'created_at': self.created_at.strftime('%b %d, %Y'),
            'updated_at': self.updated_at,
            'is_publish': self.is_publish,
            'is_featured': self.is_featured,
            'user_id': self.user_id
        }
