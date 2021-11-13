from flask import Flask


app = Flask(__name__)


@app.route('/')
def hello_world():
    return '<p>Hello, World!</p>'


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
