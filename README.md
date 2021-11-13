# summarizer

Dead simple summarization API


### How do I set this up?

* git clone git@github.com:g4b1nagy/summarizer.git
* cd summarizer/
* python3 -m venv venv
* source venv/bin/activate
* pip install -r requirements.txt
* python -c 'from summarizer import db;db.create_all()'
* FLASK_APP=summarizer FLASK_ENV=development flask run
* go to http://localhost:5000/
