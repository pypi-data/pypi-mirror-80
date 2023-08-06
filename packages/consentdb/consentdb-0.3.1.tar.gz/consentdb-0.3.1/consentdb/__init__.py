"""Top-level package for Consent database."""
__author__ = """Sjoerd Kerkstra"""
__email__ = 'sjoerd.kerkstra@radboudumc.nl'
__version__ = '0.3.1'

from os import environ
from flask import Flask
from consentdb.consentdb import consentdb_blueprint


def create_app():
    """Init main flask applications and database"""
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('SQLALCHEMY_DATABASE_URI','sqlite:///:memory:')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    from consentdb.models import db
    db.init_app(app)
    app.app_context().push()
    db.create_all()

    app.register_blueprint(consentdb_blueprint)
    return app




