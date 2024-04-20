import os
from flask import Flask, jsonify, redirect, render_template, url_for
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, current_user, login_required
from werkzeug.exceptions import Unauthorized

db = SQLAlchemy()
migrate = Migrate()
loginManager = LoginManager()

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_object('config.Config')
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)
    
    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # Initialiations
    db.init_app(app)
    migrate.init_app(app, db)
    loginManager.init_app(app)

    # Import models (must after db init)
    from . import models

    # Register blueprints for views
    from . import auth
    from . import profile
    from . import post
    from . import index
    app.register_blueprint(auth.bp)
    app.register_blueprint(profile.bp)
    app.register_blueprint(post.bp)
    app.register_blueprint(index.bp)

    # If user is not authenticated, redirect to signin page
    @app.errorhandler(Unauthorized)
    def unauthorized(error):
        return redirect(url_for('auth.signin'))

    return app
