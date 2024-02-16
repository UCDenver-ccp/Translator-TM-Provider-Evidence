from flask import Flask, request
from flask_cors import CORS
from flask_caching import Cache
from sqlalchemy import select, text, insert
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


@app.route('/api/sentences/', methods=['POST'], strict_slashes=False)
@cache.cached(timeout=30)
def assertion_lookup():
    s = Session()
    if not request.is_json:
        return "{}"
    # print(request.data)
    request_dict = json.loads(request.data)
    requested_id_list = [requested_id.replace('tmkp:', '') for requested_id in request_dict['ids']]
    # print(requested_id_list)
    assertion_id_list = list(set(get_assertion_ids(s, requested_id_list)))
    # print(assertion_id_list)
    if len(assertion_id_list) == 0:
        assertion_id_list = list(set(requested_id_list))
    assertion_query_by_id = s.query(models.Assertion).filter(models.Assertion.assertion_id.in_(assertion_id_list))
    if assertion_query_by_id.count() == 0:
        return "{}"
    assertions = [get_assertion_json(assertion) for assertion in assertion_query_by_id.all()]

    return jsonpickle.encode(assertions, unpicklable=False)


def get_assertion_ids(session, id_list: list[str]) -> list[str]:
    assertion_id_query = text('SELECT DISTINCT(assertion_id) FROM evidence WHERE evidence_id IN :ids ')
    return [row for row, in session.execute(assertion_id_query, {'ids': id_list})]


def get_assertion_json(assertion) -> dict:
    output = {
        "assertion_id": assertion.assertion_id,
        "subject": assertion.subject_uniprot.uniprot if assertion.subject_uniprot else assertion.subject_curie,
        "object": assertion.object_uniprot.uniprot if assertion.object_uniprot else assertion.object_curie,
        "association": assertion.association_curie
    }
    evidence_list = []
    for evidence in assertion.evidence_list:
        is_current = False
        for version in evidence.version:
            if version.version == 2:
                is_current = True
        if not is_current:
            continue
        top_predicate = evidence.evidence_scores[0]
        for predicate in evidence.evidence_scores:
            if predicate.score > top_predicate.score:
                top_predicate = predicate
        ev = {
            "evidence_id": evidence.evidence_id,
            "sentence": evidence.sentence,
            "document_id": evidence.document_id,
            "document_zone": evidence.document_zone,
            "document_year": evidence.actual_year.year if evidence.actual_year else evidence.document_year_published,
            "subject_span_start": evidence.subject_entity.span.split('|')[0],
            "subject_span_end": evidence.subject_entity.span.split('|')[1],
            "subject_text": evidence.subject_entity.covered_text,
            "object_span_start": evidence.object_entity.span.split('|')[0],
            "object_span_end": evidence.object_entity.span.split('|')[1],
            "object_text": evidence.object_entity.covered_text,
            "predicate": top_predicate.predicate_curie,
            "score": top_predicate.score
        }
        evidence_list.append(ev)
    output["evidence_list"] = evidence_list
    return output


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

