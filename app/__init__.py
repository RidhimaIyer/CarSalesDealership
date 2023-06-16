# from flask import Flask 
from config import Config
from flask_sqlalchemy import SQLAlchemy
import connexion

db = SQLAlchemy()

def create_app(env_name = "development"):
    connexion_app = connexion.FlaskApp(__name__)
    connexion_api = super(connexion.FlaskApp, connexion_app).add_api("openapi.yml")

    app = connexion_app.app 
    app.config.from_object(Config[env_name])
    db.init_app(app)
    app.register_blueprint(connexion_api.blueprint)

    with app.app_context():
        # db.drop_all()
        from sqlalchemy.sql import text
        db.create_all()
        db.session.execute(text("pragma foreign_keys=on"))
    
    return app 





    