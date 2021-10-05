from api.tiles.donut_tile import DonutTile


class ActivityTypesTile(DonutTile):
    def __init__(self):
        self._aggregation_fields = ['exa_activity_type.keyword']

    @property
    def _id(self):
        return 'activity_types'

    @property
    def _type(self):
        return 'donut_graph'

    @property
    def _title(self):
        return 'Activity Types'

    @property
    def _short_description(self):
        return 'Activity types found in Exabeam Data Lake'

    @property
    def _description(self):
        return 'Activity types chart shows distribution of events ' \
               'that triggered log creation by its types.'

    @property
    def _tags(self):
        return ['activity_types']
