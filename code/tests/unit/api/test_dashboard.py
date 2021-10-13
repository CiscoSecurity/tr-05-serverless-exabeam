from http import HTTPStatus
from unittest.mock import patch
from collections import namedtuple

from pytest import fixture

from api.errors import INVALID_ARGUMENT
from tests.unit.api.utils import get_headers
from tests.unit.conftest import (
    mock_api_response,
    relay_response_tile_data,
    relay_response_tiles,
    relay_response_tiles_tile,
    exabeam_response_tile
)
from tests.unit.payloads_for_tests import EXPECTED_RESPONSE_OF_JWKS_ENDPOINT

WrongCall = namedtuple('WrongCall', ('endpoint', 'payload', 'message'))


def wrong_calls():
    yield WrongCall(
        '/tiles/tile',
        {'tile-id': 'some_value'},
        "{'tile_id': ['Missing data for required field.'], "
        "'tile-id': ['Unknown field.']}"
    )
    yield WrongCall(
        '/tiles/tile',
        {'tile_id': ''},
        "{'tile_id': ['Field may not be blank.']}"
    )
    yield WrongCall(
        '/tiles/tile-data',
        {'tile_id': 'some_value', 'period': 'some_period'},
        "{'period': ['Must be one of: last_24_hours, last_7_days, "
        "last_30_days.']}"
    )
    yield WrongCall(
        '/tiles/tile-data',
        {'tile-id': 'some_value', 'period': 'last_30_days'},
        "{'tile_id': ['Missing data for required field.'], "
        "'tile-id': ['Unknown field.']}"
    )
    yield WrongCall(
        '/tiles/tile-data',
        {'tile_id': '', 'period': 'last_30_days'},
        "{'tile_id': ['Field may not be blank.']}"
    )
    yield WrongCall(
        '/tiles/tile-data',
        {'tile_id': 'some_value', 'not_period': 'some_period'},
        "{'period': ['Missing data for required field.'], "
        "'not_period': ['Unknown field.']}"
    )


@fixture(
    scope='module',
    params=wrong_calls(),
    ids=lambda wrong_payload: f'{wrong_payload.endpoint}, '
                              f'{wrong_payload.payload}'
)
def wrong_call(request):
    return request.param


@fixture(scope='module')
def invalid_argument_expected_payload():
    def _make_message(message):
        return {
            'errors': [{
                'code': INVALID_ARGUMENT,
                'message': message,
                'type': 'fatal'
            }]
        }

    return _make_message


@patch('requests.get')
def test_dashboard_call_with_wrong_payload(mock_request,
                                           wrong_call, client, valid_jwt,
                                           invalid_argument_expected_payload):

    mock_request.return_value = \
        mock_api_response(payload=EXPECTED_RESPONSE_OF_JWKS_ENDPOINT)

    response = client.post(
        path=wrong_call.endpoint,
        headers=get_headers(valid_jwt()),
        json=wrong_call.payload
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json == invalid_argument_expected_payload(
        wrong_call.message
    )


SuccessCall = namedtuple('SuccessCall', ('endpoint',
                                         'payload',
                                         'exabeam_response',
                                         'relay_response'))


def success_calls():
    last_thirty_days = 'last_30_days'
    last_seven_days = 'last_7_days'
    tiles_data = [('affected_ips', last_thirty_days),
                  ('activity_types', last_thirty_days),
                  ('categories', last_thirty_days),
                  ('activity_types_per_day', last_seven_days),
                  ('categories_per_day', last_seven_days)]
    for tile_id, period in tiles_data:
        yield SuccessCall(
            '/tiles/tile-data',
            {'tile_id': tile_id, 'period': period},
            exabeam_response_tile(tile_id),
            relay_response_tile_data(tile_id)
        )
        yield SuccessCall(
            '/tiles/tile',
            {'tile_id': tile_id},
            {},
            relay_response_tiles_tile(tile_id)
        )
    yield SuccessCall(
        '/tiles',
        {},
        {},
        relay_response_tiles()
    )


@fixture(scope='module',
         params=success_calls(),
         ids=lambda call: f'POST {call.endpoint}')
def success_call(request):
    return request.param


@patch('requests.request')
@patch('requests.get')
def test_dashboard_call_success(mock_get, mock_request,
                                success_call, client, valid_jwt):
    mock_get.return_value = mock_api_response(
        payload=EXPECTED_RESPONSE_OF_JWKS_ENDPOINT
    )
    mock_request.return_value = \
        mock_api_response(payload=success_call.exabeam_response)
    response = client.post(success_call.endpoint,
                           headers=get_headers(valid_jwt()),
                           json=success_call.payload)
    assert response.status_code == HTTPStatus.OK
    if success_call.endpoint == '/tiles/tile-data':
        assert response.json['data']['data'] == success_call.relay_response
    else:
        assert response.json == success_call.relay_response
