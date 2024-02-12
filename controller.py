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
    print(request.data)
    request_dict = json.loads(request.data)
    assertion_ids = request_dict['ids']
    print(assertion_ids)
    assertion_query_by_id = s.query(models.Assertion).filter(models.Assertion.assertion_id.in_(assertion_ids))
    if assertion_query_by_id.count() == 0:
        return "{}"
    one = assertion_query_by_id.one()
    return jsonpickle.encode(one, unpicklable=False)


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

