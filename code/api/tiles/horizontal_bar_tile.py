from datetime import datetime, timezone
from abc import ABC, abstractmethod

from flask import current_app

from api.tiles.factory import AbstractTile
from api.utils import source_uri


class HorizontalBarTile(AbstractTile, ABC):
    @property
    @abstractmethod
    def _aggregation_field(self):
        """Returns a filed with help of which aggregation query is created"""

    @property
    def _periods(self):
        return ['last_7_days']

    @property
    def _type(self):
        return 'horizontal_bar_chart'

    @staticmethod
    def _data_item(timestamp, values, value, date_label):
        return {
            'key': timestamp,
            'values': values,
            'value': value,
            'label': date_label
        }

    def _value(self, key, value):
        return {
            'key': key,
            'value': value,
            'link_uri': source_uri(
                f'{self._aggregation_field.split(".")[0]}:"{key}"',
                current_app.config['URL_PARAMS_FOR_TILE'].replace('now-30d',
                                                                  'now-1d')
            )
        }

    def _data(self, visualize_data):
        data = []
        for bucket in visualize_data[self._id]['buckets']:
            timestamp = bucket.get('key')/10**3
            date = datetime.fromtimestamp(timestamp, timezone.utc).strftime('%b/%d')
            values = []
            value = 0
            for inner_bucket in bucket[self._aggregation_field]['buckets']:
                value += inner_bucket['doc_count']
                values.append(self._value(inner_bucket['key'],
                                          inner_bucket['doc_count']))
            data.append(self._data_item(bucket['key'],
                                        values,
                                        value,
                                        date))
        return data

    def _keys(self, visualize_data):
        keys = []
        for bucket in visualize_data[self._id]['buckets']:
            for inner_bucket in bucket[self._aggregation_field]['buckets']:
                if inner_bucket['key'] not in keys:
                    keys.append(inner_bucket['key'])
        return keys

    def aggregation_query(self):
        return {
            self._id: {
                'date_histogram': {
                    'field': '@timestamp',
                    'interval': '1d',
                    'time_zone': 'UTC'
                },
                'aggs': {
                    self._aggregation_field: {
                        'terms': {
                            'field': self._aggregation_field
                        }
                    }
                }
            }
        }

    def tile_data(self, visualize_data, period):
        return {
            'observed_time': self._observed_time(period),
            'valid_time': self._valid_time(period),
            'data': self._data(visualize_data),
            'cache_scope': self._cache_scope(),
            'keys': self._keys(visualize_data),
            'key_type': 'timestamp'
        }
