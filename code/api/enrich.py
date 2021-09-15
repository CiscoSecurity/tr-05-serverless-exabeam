from functools import partial

from flask import Blueprint, g

from api.schemas import ObservableSchema
from api.utils import get_json, get_jwt, jsonify_data, jsonify_result
from api.client import ExabeamClient
from api.mapping import Sighting

enrich_api = Blueprint('enrich', __name__)

get_observables = partial(get_json, schema=ObservableSchema(many=True))


@enrich_api.route('/observe/observables', methods=['POST'])
def observe_observables():
    key = get_jwt()
    observables = get_observables()

    g.sightings = []

    client = ExabeamClient(key)
    sighting_map = Sighting()
    for observable in observables:
        data = client.get_data(observable['value'])
        for data_item in data:
            sighting = sighting_map.extract(data_item, observable)
            g.sightings.append(sighting)
    return jsonify_result()


@enrich_api.route('/refer/observables', methods=['POST'])
def refer_observables():
    _ = get_jwt()
    _ = get_observables()
    return jsonify_data([])
