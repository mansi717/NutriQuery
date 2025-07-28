# create_tables.py

# First, import your Flask application instance.
# This line assumes your main application file is named app.py
from app import app

# Next, import the db object from your models.py file.
from models import db

# This is the crucial part. We use `app.app_context()` to tell Flask-SQLAlchemy
# that we are operating within the context of our Flask application.
with app.app_context():
    # The `db.create_all()` method looks at all the classes that inherit from db.Model
    # and generates the SQL CREATE TABLE statements to create them in the database.
    # It will safely skip any tables that already exist.
    db.create_all()
    print("Database tables created successfully!")