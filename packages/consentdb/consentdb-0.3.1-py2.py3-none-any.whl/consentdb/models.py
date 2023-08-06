from typing import Dict

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class ConsentRecord(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # Primary key
    pid = db.Column(db.String(80), unique=True, nullable=False)  # Patient ID
    can_use = db.Column(db.Boolean, nullable=False)  # Data use allowed?
    last_change = db.Column(db.DateTime, nullable=False)  # Last time can_use changed

    def __repr__(self):
        return f"{self.pid}, can use:{self.can_use}"

    def to_dict(self) -> Dict:
        """A dictionary representation of this record. For json output"""
        return {'pid': self.pid,
                'can_use': self.can_use,
                'last_change': self.last_change}
