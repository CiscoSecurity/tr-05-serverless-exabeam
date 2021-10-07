from functools import partial

from flask import Blueprint, g, current_app

from api.schemas import ObservableSchema
from api.utils import get_json, get_jwt, jsonify_data, jsonify_result
from api.client import ExabeamClient
from api.mapping import Sighting, source_uri

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
    observables = get_observables()

    obs_types_map = current_app.config['HUMAN_READABLE_OBSERVABLE_TYPES']
    params = current_app.config['URL_PARAMS_FOR_REFER']

    relay_output = [
        {
            'id': (
                f'ref-exabeam-search-{observable["type"].replace("_", "-")}'
                f'-{observable["value"]}'
            ),
            'title': (
                'Search for this '
                f'{obs_types_map.get(observable["type"], observable["type"])}'
            ),
            'description': (
                'Search for this '
                f'{obs_types_map.get(observable["type"], observable["type"])}'
                ' in Exabeam Data Lake'
            ),
            'url': source_uri(observable['value'], params),
            'categories': ['Search', 'Exabeam']
        }
        for observable in observables
    ]
    return jsonify_data(relay_output)
