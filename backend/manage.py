from flask import Flask
from flask_cors import CORS
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from app.models import setup_db
from app.auth.routes import auth
from app.user.routes import user


'''
setting up flask app with cors middleware and db connection
with sqlalchemy
'''
app = Flask(__name__)
setup_db(app)
CORS(app)
app.register_blueprint(auth)
app.register_blueprint(user)
# for db migration when running manage.py
manager = Manager(app)
manager.add_command('db', MigrateCommand)


if __name__ == '__main__':
    manager.run()
    app.run(host='0.0.0.0', port='5000')
