from api.tiles.donut_tile import DonutTile


class ActivityTypesTile(DonutTile):
    @property
    def _aggregation_field(self):
        return 'exa_activity_type.keyword'

    @property
    def _id(self):
        return 'activity_types'

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
