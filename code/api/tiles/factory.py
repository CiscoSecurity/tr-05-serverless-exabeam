from abc import ABC, abstractmethod
from datetime import datetime, timedelta

from flask import current_app

from api.errors import TRFormattedError

INVALID_CHART_ID = 'Invalid chart id'


class AbstractTile(ABC):
    @staticmethod
    def _observed_time(period):
        delta = timedelta(days=current_app.config['TILE_PERIODS_MAP'][period])
        today = datetime.today()

        return {
            'start_time': (today - delta).isoformat(timespec='milliseconds'),
            'end_time': datetime.now().isoformat(timespec='milliseconds')
        }

    @staticmethod
    def _valid_time(period):
        return AbstractTile._observed_time(period)

    @staticmethod
    def _cache_scope():
        return 'none'

    @abstractmethod
    def _data(self):
        """Returns data that constructs tile"""

    @property
    @abstractmethod
    def _id(self):
        """Returns tile id."""

    @property
    @abstractmethod
    def _type(self):
        """Returns tile type."""

    @property
    @abstractmethod
    def _title(self):
        """Returns tile title."""

    @property
    @abstractmethod
    def _short_description(self):
        """Returns tile short description."""

    @property
    @abstractmethod
    def _description(self):
        """Returns tile description."""

    @property
    @abstractmethod
    def _tags(self):
        """Returns tile tags."""

    @property
    @abstractmethod
    def _periods(self):
        """Returns tile available periods to represent data."""

    @abstractmethod
    def aggregation_query(self):
        """Returns query which is used
        by client to make a visualize request."""

    @abstractmethod
    def tile_data(self):
        """Returns data for /tiles/tile-data endpoint."""

    def tile(self):
        """Returns data for /tiles/tile endpoint."""
        return {
            'id': self._id,
            'type': self._type,
            'title': self._title,
            'short_description': self._short_description,
            'description': self._description,
            'tags': self._tags,
            'periods': self._periods
        }


class TileFactory:
    @staticmethod
    def create_tile(tile_id):
        for cls in TileFactory.get_leaf_subclasses(AbstractTile):
            if cls()._id == tile_id:
                return cls()
        raise TRFormattedError(400, INVALID_CHART_ID)

    @staticmethod
    def tiles_list():
        return [cls().tile()
                for cls in TileFactory.get_leaf_subclasses(AbstractTile)]

    @staticmethod
    def get_leaf_subclasses(cls):
        if cls.__subclasses__():
            subclasses_list = []
            for subcls in cls.__subclasses__():
                subclasses_list.extend(TileFactory.get_leaf_subclasses(subcls))
            return subclasses_list
        return [cls]
