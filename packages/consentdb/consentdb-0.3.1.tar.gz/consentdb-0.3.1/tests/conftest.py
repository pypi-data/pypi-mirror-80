"""Conftest.py is loaded for each pytest. Contains fixtures shared by multiple tests
"""
import pytest
from consentdb import create_app


@pytest.fixture(scope='module')
def test_client():
    """A flask test client with some debug settings."""
    flask_app = create_app()

    # Bcrypt algorithm hashing rounds (reduced for testing purposes only!)
    flask_app.config['BCRYPT_LOG_ROUNDS'] = 4

    # Disable request error catching
    flask_app.config['TESTING'] = True

    # Disable CSRF tokens in the Forms (only valid for testing purposes!)
    flask_app.config['WTF_CSRF_ENABLED'] = False

    # expose built the Werkzeug test Client and handle context locals
    testing_client = flask_app.test_client()

    # Establish an application context before running the tests.
    ctx = flask_app.app_context()
    ctx.push()

    yield testing_client  # this is where the testing happens!

    ctx.pop()