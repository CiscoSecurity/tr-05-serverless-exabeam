import json

from flask import Blueprint, current_app

from api.utils import jsonify_data, get_jwt, get_json
from api.schemas import DashboardTileSchema, DashboardTileDataSchema
from api.tiles.factory import TileFactory
from api.client import ExabeamClient

dashboard_api = Blueprint('dashboard', __name__)


@dashboard_api.route('/tiles', methods=['POST'])
def tiles():
    _ = get_jwt()
    tiles_list = TileFactory.tiles_list()
    return jsonify_data(tiles_list)


@dashboard_api.route('/tiles/tile', methods=['POST'])
def tile():
    _ = get_jwt()
    payload = get_json(DashboardTileSchema())
    tile_object = TileFactory.create_tile(payload['tile_id'])
    return jsonify_data(tile_object.tile())


@dashboard_api.route('/tiles/tile-data', methods=['POST'])
def tile_data():
    key = get_jwt()
    payload = get_json(DashboardTileDataSchema())
    tile_object = TileFactory.create_tile(payload['tile_id'])
    aggregation_query = tile_object.aggregation_query()
    client = ExabeamClient(key)
    visualize_data = client.get_visualize_data(
        json.dumps(aggregation_query),
        current_app.config['TILE_PERIODS_MAP'][payload['period']]
    )
    return jsonify_data(tile_object.tile_data(visualize_data,
                                              payload['period']))
