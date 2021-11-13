import datetime

from flask import Flask
from flask_sqlalchemy import SQLAlchemy


# =========================================================================
# Setup and configuration
# =========================================================================

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'

# Only needed if you need to get notified before and after changes are committed to the database.
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# =========================================================================
# Models
# =========================================================================

class Document(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    created = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow)
    updated = db.Column(db.DateTime, onupdate=datetime.datetime.utcnow)
    text = db.Column(db.Text, nullable=False)
    summary = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return f'<Document {self.id}>'

# =========================================================================
# Health check route
# =========================================================================

@app.route('/')
def hello_world():
    return '<p>Hello, World!</p>'

# =========================================================================
# RESTful API document routes
# =========================================================================

# This, of course, is a very verbose and naive way of building the routes.
# Something more structured, such as Flask-RESTful, would be preferable.

@app.route('/document/<int:document_id>', methods=['GET'])
def document_get(document_id):
    """Retrieve the document with the given id."""
    pass


# If you access the URL without a trailing slash,
# Flask redirects you to the canonical URL with the trailing slash.
@app.route('/document/', methods=['POST'])
def document_post():
    """Create a new document and return its id."""
    pass


@app.route('/document/<int:document_id>', methods=['PUT'])
def document_put(document_id):
    """Create or update the document with the given id."""
    pass


@app.route('/document/<int:document_id>', methods=['DELETE'])
def document_delete(document_id):
    """Delete the document with the given id."""
    pass
