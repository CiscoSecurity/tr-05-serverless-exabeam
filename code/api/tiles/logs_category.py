from api.tiles.donut_tile import DonutTile


class CategoriesTile(DonutTile):
    @property
    def _aggregation_field(self):
        return 'exa_category.keyword'

    @property
    def _id(self):
        return 'categories'

    @property
    def _title(self):
        return 'Categories'

    @property
    def _short_description(self):
        return 'Log categories found in Exabeam Data Lake'

    @property
    def _description(self):
        return 'Log categories chart shows distribution of logs ' \
               'by its categories.'
