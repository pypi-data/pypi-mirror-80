"""
Examples on testing flaske with pytest and copied from https://gitlab.com/patkennedy79
"""
import pytest

from consentdb.admin import add_records
from consentdb.models import db, ConsentRecord
from tests.factories import ConsentRecordFactory


@pytest.fixture(scope='module')
def init_test_database():
    """Init database and add some test data"""
    # Create the database and the database table
    db.create_all()

    yield db  # this is where the testing happens!

    db.drop_all()


def test_add(test_client, init_test_database):

    add_records([ConsentRecordFactory(),
                 ConsentRecordFactory(),
                 ConsentRecordFactory()])

    assert len(ConsentRecord.query.all()) == 3