import os
from flask import Flask, jsonify, render_template
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
migrate = Migrate()

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

    # Initialize database and migration
    db.init_app(app)
    migrate.init_app(app, db)

    # Import models
    from app import models

    @app.route("/")
    def index():
        return render_template("index.html")

    return app
