from flask import request, jsonify
from flask.blueprints import Blueprint
from flask.helpers import url_for

from consentdb.models import ConsentRecord

# Blueprint instead of direct app() for easier testing
consentdb_blueprint = Blueprint('consentdb', __name__)


@consentdb_blueprint.route('/')
def index():
    return "consent db API"


@consentdb_blueprint.route('/opt-outs/', strict_slashes=False)
def opt_out():
    pid = request.args.get('pid')
    if not pid:
        return "Error - Please specify PID using ?pid=", 400
    record = ConsentRecord.query.filter_by(pid=pid).first()
    if not record:
        return "not listed"
    if record.can_use:
        return "not listed"
    else:
        return "objection"


@consentdb_blueprint.route('/opt-out-info')
def opt_out_info():
    return f"V1 API (opt-out), use {url_for('consentdb.opt_out', pid='z1234567')}."


@consentdb_blueprint.route('/consent/')
def consent_info():
    return f"Missing patient ID. Please " \
           f"use {url_for('consentdb.consent', pid='1234567')}.", 400


@consentdb_blueprint.route('/consent/<string:pid>')
def consent(pid):
    record = ConsentRecord.query.filter_by(pid=pid).first()
    if record:
        return jsonify(record.to_dict())
    else:
        return {}, 400

