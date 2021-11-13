import datetime

from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import inspect
from sumy.nlp.stemmers import Stemmer
from sumy.nlp.tokenizers import Tokenizer
from sumy.parsers.plaintext import PlaintextParser
from sumy.summarizers.lsa import LsaSummarizer
from sumy.utils import get_stop_words


# =========================================================================
# Setup and configuration
# =========================================================================

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'

# Only needed if you need to get notified before and after changes are committed to the database.
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SUMMARIZATION_LANGUAGE'] = 'english'
app.config['SUMMARIZATION_SENTENCE_COUNT'] = 3
db = SQLAlchemy(app)
tokenizer = Tokenizer(app.config['SUMMARIZATION_LANGUAGE'])
stemmer = Stemmer(app.config['SUMMARIZATION_LANGUAGE'])
summarizer = LsaSummarizer(stemmer)
summarizer.stop_words = get_stop_words(app.config['SUMMARIZATION_LANGUAGE'])

# =========================================================================
# Models
# =========================================================================

class Document(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    created = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow)
    updated = db.Column(db.DateTime, onupdate=datetime.datetime.utcnow)
    text = db.Column(db.Text, nullable=False)
    summary = db.Column(db.Text, nullable=False)

    def to_json(self):
        data = {column.key: getattr(self, column.key) for column in inspect(self).mapper.column_attrs}
        for key, value in data.items():
            if isinstance(value, datetime.datetime) or isinstance(value, datetime.date):
                data[key] = value.isoformat()
        return data

    def __repr__(self):
        return f'<Document {self.id}>'


def get_summary(text, sentence_count=app.config['SUMMARIZATION_SENTENCE_COUNT']):
    parser = PlaintextParser.from_string(text, tokenizer)
    sentences = summarizer(parser.document, sentence_count)
    summary = ' '.join([str(x) for x in sentences])
    return summary

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

    document = db.session.query(Document).get(document_id)
    if document is None:
        return jsonify(message=f'No document with id {document_id} found.'), 404
    else:
        return jsonify(document.to_json())


# If you access the URL without a trailing slash,
# Flask redirects you to the canonical URL with the trailing slash.
@app.route('/document/', methods=['POST'])
def document_post():
    """Create a new document and return its id."""

    # The request Content-Type may be either
    # application/json or
    # application/x-www-form-urlencoded
    json_data = request.get_json()
    if json_data is not None:
        text = json_data.get('text')
    else:
        text = request.form.get('text')
    if text is None:
        return jsonify(message='Missing required field: text'), 400
    else:
        document = Document(text=text, summary=get_summary(text))
        db.session.add(document)
        db.session.commit()
        return jsonify(document_id=document.id)


@app.route('/document/<int:document_id>', methods=['PUT'])
def document_put(document_id):
    """Create or update the document with the given id."""

    # The request Content-Type may be either
    # application/json or
    # application/x-www-form-urlencoded
    json_data = request.get_json()
    if json_data is not None:
        text = json_data.get('text')
    else:
        text = request.form.get('text')
    if text is None:
        return jsonify(message='Missing required field: text'), 400
    else:
        document = db.session.query(Document).get(document_id) or Document()
        document.id = document_id
        document.text = text
        document.summary = get_summary(text)
        db.session.add(document)
        db.session.commit()
        return jsonify(document_id=document.id)


@app.route('/document/<int:document_id>', methods=['DELETE'])
def document_delete(document_id):
    """Delete the document with the given id."""

    document = db.session.query(Document).get(document_id)
    if document is None:
        return jsonify(message=f'No document with id {document_id} found.'), 404
    else:
        db.session.delete(document)
        db.session.commit()
        return jsonify(message='OK')


@app.route('/document/<int:document_id>/summary/', methods=['GET'])
def document_get_summary(document_id):
    """Retrieve the summary of the document with the given id."""

    document = db.session.query(Document).get(document_id)
    if document is None:
        return jsonify(message=f'No document with id {document_id} found.'), 404
    else:
        return jsonify(summary=document.summary)
