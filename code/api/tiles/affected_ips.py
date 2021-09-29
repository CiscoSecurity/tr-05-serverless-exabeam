from flask import current_app

from api.tiles.factory import AbstractTile
from api.utils import source_uri


class AffectedIPsTile(AbstractTile):
    def __init__(self):
        self._aggregation_fields = {
            'is_ransomware_src_ip': 'Ransomware IPs',
            'is_threat_src_ip': 'Threat IPs',
            'is_tor_src_ip': 'Tor IPs'
        }

    @property
    def _id(self):
        return 'affected_ips'

    @property
    def _type(self):
        return 'metric_group'

    @property
    def _title(self):
        return 'Affected IPs'

    @property
    def _short_description(self):
        return 'Affected IPs found in Exabeam Data Lake'

    @property
    def _description(self):
        return 'Affected IPs chart shows how many IPs are ransomware, ' \
               'threat or tor'

    @property
    def _tags(self):
        return ['affected_ips']

    @property
    def _periods(self):
        return ['last_30_days']

    @staticmethod
    def _data_item(field, label, value):
        return {
            'icon': 'warning',
            'label': label,
            'value': value,
            'value_unit': 'integer',
            'link_uri': source_uri(
                f'{field}:"true"',
                current_app.config['URL_PARAMS_FOR_TILE']
            )
        }

    def _data(self, visualize_data):
        data = []
        for field, label in self._aggregation_fields.items():
            value = 0
            for bucket in visualize_data[field]['buckets']:
                if bucket.get('key'):
                    value = bucket['doc_count']
            data.append(self._data_item(field, label, value))

        return data

    def aggregation_query(self):
        aggregation_query = {field: {'terms': {'field': field}}
                             for field in self._aggregation_fields}
        return aggregation_query

    def tile_data(self, visualize_data, period):
        return {
            'observed_time': self._observed_time(period),
            'valid_time': self._valid_time(period),
            'data': self._data(visualize_data),
            'cache_scope': self._cache_scope()
        }
