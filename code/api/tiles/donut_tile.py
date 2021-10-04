from abc import ABC, abstractmethod

from flask import current_app

from api.tiles.factory import AbstractTile
from api.utils import source_uri


class DonutTile(AbstractTile, ABC):
    @property
    @abstractmethod
    def _aggregation_field(self):
        """Returns a field with help of which aggregation query is created"""

    @property
    def _type(self):
        return 'donut_graph'

    @property
    def _periods(self):
        return ['last_30_days']

    @staticmethod
    def _data_item(label_index, value, field, field_value):
        return {
            'key': label_index,
            'value': value,
            'link_uri': source_uri(
                f'{field.split(".")[0]}:"{field_value}"',
                current_app.config['URL_PARAMS_FOR_TILE']
            )
        }

    def _data(self, visualize_data):
        data = []
        labels = self._labels(visualize_data)[0]
        for bucket in visualize_data[self._aggregation_field]['buckets']:
            data.append(self._data_item(labels.index(bucket.get('key')),
                                        bucket['doc_count'],
                                        self._aggregation_field,
                                        bucket.get('key')))
        return data

    def _labels(self, visualize_data):
        labels = []
        label_column = []
        for bucket in visualize_data[self._aggregation_field]['buckets']:
            label_column.append(bucket.get('key'))
        labels.append(label_column)
        return labels

    def aggregation_query(self):
        return {
            self._aggregation_field: {
                'terms': {
                    'field': self._aggregation_field
                }
            }
        }

    def tile_data(self, visualize_data, period):
        return {
            'observed_time': self._observed_time(period),
            'valid_time': self._valid_time(period),
            'data': self._data(visualize_data),
            'labels': self._labels(visualize_data),
            'cache_scope': self._cache_scope()
        }
