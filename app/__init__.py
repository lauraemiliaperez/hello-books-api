from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from dotenv import load_dotenv
import os

db = SQLAlchemy()
migrate = Migrate()
load_dotenv()

#we say to the app where to get the endpoints

def create_app(test_config=None):
    app = Flask(__name__)

    
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        # app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('SQLALCHEMY_DATABASE_URI')
    # else:
    #     app.config["TESTING"] = True
    #     app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get(
            'RENDER_DATABASE_URI')

    
    db.init_app(app)
    migrate.init_app(app, db)
    
    from app.models.book import Book
    from app.models.author import Author

    from .route import books_bp
    from .route import authors_bp
    app.register_blueprint(books_bp)
    app.register_blueprint(authors_bp)
    

    return app
