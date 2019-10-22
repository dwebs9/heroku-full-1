from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
import os
from flask_login import LoginManager

db = SQLAlchemy()

# create a function that creates a web application
# a web server will run this web application


def create_app():

    # this is the name of the module/package that is calling this app
    app = Flask(__name__)
    app.debug = True
    app.secret_key = "utroutoru"
    # set the app configuration data
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///marketplace.sqlite"
    # Flask-SQLAlchemy settings

    # app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']

    # initialize db with flask app
    db.init_app(app)

    bootstrap = Bootstrap(app)

    # initialize the login manager
    login_manager = LoginManager()

    # set the name of the login function that lets user login
    # in our case it is auth.login (blueprintname.viewfunction name)
    login_manager.login_view = "auth.login"
    login_manager.init_app(app)

    # create a user loader function takes userid and returns User
    from .models import User  # importing here to avoid circular references

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # importing views module here to avoid circular references
    # a commonly used practice.
    from . import views

    app.register_blueprint(views.bp)

    from . import auth

    app.register_blueprint(auth.bp)

    from . import tools
    app.register_blueprint(tools.bp)

    from . import userdash
    app.register_blueprint(userdash.bp)

    @app.errorhandler(404)
    def not_found(e):
        heading = "404"
        image = "static/img/404.png"

        return render_template("error.html", heading=heading, image=image), 404

    @app.errorhandler(500)
    def server_error(e):
        heading = "500, Internal Server Error"
        image = "static/img/500.png"
        return render_template("error.html", heading=heading, image=image), 500

    return app
