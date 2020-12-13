import logging.config
import os

from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import event
from sqlalchemy.engine import Engine

from src.system.utils.file import delete_file, write_file

logging.config.fileConfig('logging/logging.conf')

app = Flask(__name__)
CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

if not os.environ.get("data_dir"):
    url = 'sqlite:///data.db?timeout=60'
else:
    url = f'sqlite:///{os.environ.get("data_dir")}/data.db?timeout=60'

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', url)


@event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()


app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = False  # for print the sql query

db = SQLAlchemy(app)

# add/update/delete token
token = os.environ.get("token")
auth_file = 'auth'
if token:
    write_file(auth_file, token)
else:
    delete_file(auth_file)

from src import routes  # importing for creating all the schema on un-existing case

db.create_all()
