import random

from flask import Flask, request
from flask_cors import CORS
from flask_caching import Cache
from sqlalchemy import text
from sqlalchemy.orm.scoping import scoped_session
import os
import models
import json
import jsonpickle

config = {
    "DEBUG": True,
    "CACHE_TYPE": "SimpleCache",
    "CACHE_DEFAULT_TIMEOUT": 300
}
app = Flask(__name__, static_folder='public')
app.config.from_mapping(config)
cache = Cache(app)
CORS(app)


@app.route('/version/', strict_slashes=False)
def version():
    return '0.0.1'


@app.route('/', strict_slashes=False)
def health_check():
    s = Session()
    assertion_id_query = text('SELECT assertion_id FROM assertion ORDER BY RAND() LIMIT 10')
    assertions_id_list = [row for row, in s.execute(assertion_id_query)]
    sample_id_list = random.sample(assertions_id_list, 5)
    return sample_id_list


@app.route('/api/sentences/', methods=['POST'], strict_slashes=False)
def assertion_lookup():
    s = Session()
    if not request.is_json:
        return "{}"
    # print(request.data)
    request_dict = json.loads(request.data)
    if 'ids' not in request_dict:
        return '{}'
    requested_id_list = [requested_id.replace('tmkp:', '') for requested_id in request_dict['ids']]
    evidence_limit = request_dict['limit'] if 'limit' in request_dict and isinstance(request_dict['limit'], int) else 0
    score_threshold = request_dict['threshold'] if 'threshold' in request_dict and isinstance(request_dict['threshold'], float) else 0.0
    assertion_id_list = list(set(get_assertion_ids(s, requested_id_list)))
    if len(assertion_id_list) == 0:
        assertion_id_list = list(set(requested_id_list))
    assertion_query_by_id = s.query(models.Assertion).filter(models.Assertion.assertion_id.in_(assertion_id_list))
    if assertion_query_by_id.count() == 0:
        return "{}"
    assertions = [get_assertion_json(assertion, limit=evidence_limit, threshold=score_threshold)
                  for assertion in assertion_query_by_id.all()]

    return jsonpickle.encode([a for a in assertions if len(a['evidence_list']) > 0], unpicklable=False)


def get_assertion_ids(session, id_list: list[str]) -> list[str]:
    assertion_id_query = text('SELECT DISTINCT(assertion_id) FROM evidence WHERE evidence_id IN :ids ')
    return [row for row, in session.execute(assertion_id_query, {'ids': id_list})]


#todo add the type hint for the return value
def get_assertion_json(assertion, limit=5, threshold=0):
    output = {
        "assertion_id": assertion.assertion_id,
        "subject": assertion.subject_curie,
        "object": assertion.object_curie,
        "association": assertion.association_curie
    }
    evidence_list = []
    assertion.evidence_list.sort(key=lambda x: x.score, reverse=True)
    # print([ev.score for ev in assertion.evidence_list[:5]])
    for evidence in assertion.evidence_list:
        if threshold > 0 and evidence.score < threshold:
            continue
        if 0 < limit <= len(evidence_list):
            break
        if evidence.document_zone == 'reference':
            continue
        ev = {
            "evidence_id": evidence.evidence_id,
            "sentence": evidence.sentence,
            "document_id": evidence.document_id,
            "document_zone": evidence.document_zone,
            "document_year": evidence.document_year_published,
            "subject_span_start": evidence.subject_span.split('|')[0],
            "subject_span_end": evidence.subject_span.split('|')[1],
            "subject_text": evidence.subject_covered_text,
            "object_span_start": evidence.object_span.split('|')[0],
            "object_span_end": evidence.object_span.split('|')[1],
            "object_text": evidence.object_covered_text,
            "predicate": evidence.predicate_curie,
            "score": evidence.score
        }
        evidence_list.append(ev)
    output["evidence_list"] = evidence_list
    return output


@app.teardown_appcontext
def shutdown_session(response_or_exc):
    Session.remove()


username = os.getenv('MYSQL_DATABASE_USER', None)
secret_password = os.getenv('MYSQL_DATABASE_PASSWORD', None)
EDGE_LIMIT = int(os.getenv('EDGE_LIMIT', '500'))
TMUI_ID = 0
assert username
assert secret_password
models.init_db(username=username, password=secret_password)
Session = scoped_session(models.Session)

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))

