from http import HTTPStatus
from unittest.mock import patch

from pytest import fixture, mark

from tests.unit.api.utils import get_headers
from tests.unit.conftest import mock_api_response
from tests.unit.payloads_for_tests import EXPECTED_RESPONSE_OF_JWKS_ENDPOINT


OBSERVE_ROUTE = '/observe/observables'
REFER_ROUTE = '/refer/observables'


@fixture(scope='module')
def invalid_json_value():
    return [{'type': 'ip', 'value': ''}]


@mark.parametrize(
    'route',
    [OBSERVE_ROUTE, REFER_ROUTE],
)
@patch('requests.get')
def test_enrich_call_with_valid_jwt_but_invalid_json_value(
        mock_request, route, client, valid_jwt, invalid_json_value,
        invalid_json_expected_payload
):
    mock_request.return_value = \
        mock_api_response(payload=EXPECTED_RESPONSE_OF_JWKS_ENDPOINT)
    response = client.post(route,
                           headers=get_headers(valid_jwt()),
                           json=invalid_json_value)
    assert response.status_code == HTTPStatus.OK
    assert response.json == invalid_json_expected_payload(
        "{0: {'value': ['Field may not be blank.']}}"
    )


@fixture(scope='module')
def valid_json():
    return [{'type': 'domain', 'value': 'cisco.com'}]


@patch('requests.request')
@patch('requests.get')
def test_enrich_call_success(
        mock_get, mock_request, expected_exabeam_response,
        client, valid_jwt, valid_json, expected_relay_response
):
    mock_get.return_value = \
        mock_api_response(payload=EXPECTED_RESPONSE_OF_JWKS_ENDPOINT)
    mock_request.return_value = \
        mock_api_response(payload=expected_exabeam_response)
    response = client.post(OBSERVE_ROUTE, headers=get_headers(valid_jwt()),
                           json=valid_json)
    assert response.status_code == HTTPStatus.OK
    assert response.json == expected_relay_response(OBSERVE_ROUTE)


@patch('requests.request')
@patch('requests.get')
def test_enrich_call_with_bad_request_error(
        mock_get, mock_request, client,
        valid_jwt, valid_json, bad_request_expected_relay_response
):
    mock_get.return_value = \
        mock_api_response(payload=EXPECTED_RESPONSE_OF_JWKS_ENDPOINT)
    mock_request.return_value = mock_api_response(
        text='Bad request to Exabeam',
        status_code=HTTPStatus.BAD_REQUEST)

    response = client.post(OBSERVE_ROUTE,
                           headers=get_headers(valid_jwt()),
                           json=valid_json)
    assert response.status_code == HTTPStatus.OK
    assert response.json == bad_request_expected_relay_response
