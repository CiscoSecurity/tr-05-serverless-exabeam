from api.tiles.horizontal_bar_tile import HorizontalBarTile


class CategoriesPerDayTile(HorizontalBarTile):
    @property
    def _aggregation_field(self):
        return 'exa_category.keyword'

    @property
    def _id(self):
        return 'categories_per_day'

    @property
    def _title(self):
        return 'Categories per day'

    @property
    def _short_description(self):
        return 'Categories found in Exabeam Data Lake per day'

    @property
    def _description(self):
        return f'{self._title} chart shows dynamic of log categories ' \
               'found in Exabeam Data Lake for the last 7 days'
