import os 

basedir = os.path.abspath(os.path.dirname(__name__))

class Development:
    SQLALCHEMY_DATABASE_URI = os.getenv("SQLALCHEMY_DATABASE_URL") or "sqlite:///" + os.path.join(basedir, "database.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False 
    SECRET_KEY = "2710e199-b937-44c6-af14-bd6b3c697dbb" # uuid4 generated
    FLASK_ENV = os.getenv('FLASK_ENV', 'development')
    DEBUG=True


Config= {
    "development": Development
}