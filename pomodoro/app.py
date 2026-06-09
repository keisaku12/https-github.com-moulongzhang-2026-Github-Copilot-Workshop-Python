from flask import Flask, render_template
from .config import DevelopmentConfig, ProductionConfig, TestingConfig
from .models import db


def create_app(config_name: str = "development") -> Flask:
    app = Flask(
        __name__,
        template_folder="templates",
        static_folder="static",
        static_url_path="/static",
    )

    if config_name == "production":
        app.config.from_object(ProductionConfig)
    elif config_name == "testing":
        app.config.from_object(TestingConfig)
    else:
        app.config.from_object(DevelopmentConfig)

    db.init_app(app)

    @app.route("/")
    def index():
        return render_template("index.html")

    return app
