from uuid import uuid5, NAMESPACE_X500

from flask import current_app

from api.utils import source_uri

SIGHTING = 'sighting'

SOURCE = 'Exabeam'
CONFIDENCE = 'High'
SCHEMA_VERSION = '1.1.7'

SIGHTING_DEFAULTS = {
    'confidence': CONFIDENCE,
    'schema_version': SCHEMA_VERSION,
    'source': SOURCE,
    'type': SIGHTING,
    'title': 'Log message received by Exabeam in last 30 days contains '
             'observable',
    'internal': True,
    'count': 1
}


class Sighting:
    def _sighting(self, data, observable):
        sighting = {
            'description': f'```\n{data.get("_source", {}).get("message")}'
                           '\n```',
            'short_description': self._short_description(
                data.get('_source', {})
            ),
            'external_ids': [
                data.get('_id')
            ],
            'id': self._transient_id(data.get('_source', {}), observable),
            'observables': [observable],
            'observed_time': {
                'start_time': data.get('_source', {}).get('exa_rawEventTime')
            },
            'data': self._data_table(data),
            'source_uri': self.sighting_source_uri(data.get('_id', {})),
            **SIGHTING_DEFAULTS
        }

        return sighting

    @staticmethod
    def _transient_id(data, observable):
        seeds = f'{SOURCE}|{observable["value"]}|' \
                f'{data.get("exa_rawEventTime")}|' \
                f'{data.get("message")}'
        sighting_id = f'transient:{SIGHTING}-{uuid5(NAMESPACE_X500, seeds)}'
        return sighting_id

    @staticmethod
    def sighting_source_uri(value):
        params = current_app.config['URL_PARAMS_FOR_SIGHTING']
        return source_uri(value, params)

    @staticmethod
    def _short_description(data):
        return f'Exabeam received a log from {data.get("forwarder")} ' \
               'containing the observable'

    @staticmethod
    def _data_table(data):
        data_table = {
            'columns': [],
            'rows': [[]]
        }

        for key, value in data.get('_source', {}).items():
            key_check = key.startswith(('_', 'exa_', '@')) \
                        or key in ['message', 'Product', 'Vendor']
            if not key_check and value:
                data_table['columns'].append({'name': key, 'type': 'string'})
                data_table['rows'][0].append(value)

        return data_table

    def extract(self, data, observable):
        sighting = self._sighting(data, observable)
        return sighting
