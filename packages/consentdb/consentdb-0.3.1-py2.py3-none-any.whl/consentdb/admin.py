""" Admin functions
"""
from typing import List

from consentdb.models import ConsentRecord, db


def add_records(records: List[ConsentRecord]):
    """Add all records to main db

    Raises
    ------
    SQLAlchemyError:
        if anything goes wrong inserting records

    """
    for record in records:
        db.session.add(record)
    db.session.commit()
    print(f'Added {len(records)} records')