from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from .settings import DATABASE, HOST, DB_PASSWORD, DB_USER, DB_NAME


db = SQLAlchemy()


def setup_db(app):
    app.config['SQLALCHEMY_DATABASE_URI'] = f'{DATABASE}://{DB_USER}:{DB_PASSWORD}@{HOST}/{DB_NAME}'
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    migrate = Migrate(app, db)
    db.init_app(app)
