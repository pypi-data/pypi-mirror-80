from datetime import datetime

import factory.fuzzy
from consentdb.models import ConsentRecord


class ConsentRecordFactory(factory.Factory):
    class Meta:
        model = ConsentRecord

    pid = factory.Sequence(lambda n: f"z{n:07d}")
    can_use = factory.fuzzy.FuzzyChoice([True, False])
    last_change = factory.fuzzy.FuzzyDate(datetime(year=2010, month=1, day=1),
                                          datetime(year=2020, month=5, day=1))

