from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from flask_login import LoginManager
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from config import config

bootstrap = Bootstrap()
moment = Moment()
db = SQLAlchemy()
migrate = Migrate(db)
login_manager = LoginManager()
login_manager.login_view = 'auth.login'


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])  # make the configuration according to the config_name
    config[config_name].init_app(app)

    # initialize the Flask extensions
    bootstrap.init_app(app)
    moment.init_app(app)
    db.init_app(app)
    migrate.init_app(app)
    login_manager.init_app(app)

    # main blueprint registration
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    # auth blueprint registration
    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/auth')

    # dormAdmin blueprint registration
    from .dormAdmin import dormAdmin as dormAdmin_blueprint
    app.register_blueprint(dormAdmin_blueprint, url_prefix='/dormAdmin')

    # sysAdmin blueprint registration
    from .sysAdmin import sysAdmin as sysAdmin_blueprint
    app.register_blueprint(sysAdmin_blueprint, url_prefix='/sysAdmin')

    return app


