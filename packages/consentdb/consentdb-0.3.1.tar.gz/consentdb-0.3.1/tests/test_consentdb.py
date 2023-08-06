"""
Examples on testing flaske with pytest and copied from https://gitlab.com/patkennedy79
"""
from datetime import datetime

import pytest
from consentdb.models import db, ConsentRecord


@pytest.fixture(scope='module')
def init_test_database():
    """Init database and add some test data"""
    # Create the database and the database table
    db.create_all()

    # Create some records
    db.session.add(ConsentRecord(pid='01234', can_use=True,
                                 last_change=datetime(year=2010, month=1, day=1)))
    db.session.add(ConsentRecord(pid='012345', can_use=False,
                                 last_change=datetime(year=2020, month=2, day=13)))
    db.session.commit()

    yield db  # this is where the testing happens!

    db.drop_all()


@pytest.mark.parametrize("url, expected_status, expected_data",
                         [('/opt-outs/', 400, b'Error - Please specify PID'),
                          ('/opt-outs', 400, b'Error - Please specify PID'),
                          ('/opt-outs/?pid=x1234', 200, b'not listed'),
                          ('/opt-outs/?pid=01234', 200, b'not listed'),
                          ('/opt-outs/?pid=012345', 200, b'objection'),
                          ('/opt-outs?pid=012345', 200, b'objection')])
def test_opt_out(test_client, init_test_database, url, expected_status,
                 expected_data):
    """Test expected responses for old opt-out system

    This should return
    200 'not listed' if there is no objection
    200 'objection' if there is
    400 'Error' if you don't specify ?pid=
    """
    assert test_client.get(url).status_code == expected_status
    assert expected_data in test_client.get(url).data


@pytest.mark.parametrize("url, expected_status, expected_data",
                         [('/consent/01234', 200, True),
                          ('/consent/012345', 200, False)])
def test_consent(test_client, init_test_database, url, expected_status,
                 expected_data):
    """Test expected responses for old opt-out system

    This should return
    200 'not listed' if there is no objection
    200 'objection' if there is
    400 'Error' if you don't specify ?pid=
    """
    assert test_client.get(url).status_code == expected_status
    assert test_client.get(url).json['can_use'] == expected_data


@pytest.mark.parametrize("url, expected_status, expected_data",
                         [('/consent/', 400,
                           b"Missing patient ID. Please use /consent/1234567."),
                          ('/consent/x1234', 400, b'{}\n')])
def test_consent_errors(test_client, init_test_database, url, expected_status,
                        expected_data):
    """Test expected responses for old opt-out system

    This should return
    200 'not listed' if there is no objection
    200 'objection' if there is
    400 'Error' if you don't specify ?pid=
    """
    assert test_client.get(url).status_code == expected_status
    assert test_client.get(url).data == expected_data
