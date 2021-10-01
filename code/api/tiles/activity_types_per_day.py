from api.tiles.horizontal_bar_tile import HorizontalBarTile


class ActivityTypePerDayTile(HorizontalBarTile):
    def __init__(self):
        self._aggregation_field = 'exa_activity_type.keyword'

    @property
    def _id(self):
        return 'activity_types_per_day'

    @property
    def _title(self):
        return 'Activity types per day'

    @property
    def _short_description(self):
        return 'Activity types found in Exabeam Data Lake per day'

    @property
    def _description(self):
        return f'{self._title} chart shows dynamic of activity types ' \
               'found in Exabeam Data Lake for the last 7 days'

    @property
    def _tags(self):
        return [self._id]
