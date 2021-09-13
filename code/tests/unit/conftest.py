from http import HTTPStatus
from unittest.mock import MagicMock

import jwt
from pytest import fixture

from app import app
from api.errors import INVALID_ARGUMENT
from tests.unit.payloads_for_tests import PRIVATE_KEY


@fixture(scope='session')
def client():
    app.rsa_private_key = PRIVATE_KEY

    app.testing = True

    with app.test_client() as client:
        yield client


@fixture(scope='session')
def valid_jwt(client):
    def _make_jwt(
            key='some_key',
            host='exabeam.com',
            jwks_host='visibility.amp.cisco.com',
            aud='http://localhost',
            kid='02B1174234C29F8EFB69911438F597FF3FFEE6B7',
            wrong_structure=False,
            wrong_jwks_host=False
    ):
        payload = {
            'key': key,
            'host': host,
            'jwks_host': jwks_host,
            'aud': aud,
        }

        if wrong_jwks_host:
            payload.pop('jwks_host')

        if wrong_structure:
            payload.pop('key')

        return jwt.encode(
            payload, client.application.rsa_private_key, algorithm='RS256',
            headers={
                'kid': kid
            }
        )

    return _make_jwt


@fixture(scope='module')
def invalid_json_expected_payload():
    def _make_message(message):
        return {
            'errors': [{
                'code': INVALID_ARGUMENT,
                'message': message,
                'type': 'fatal'
            }]
        }

    return _make_message


def mock_api_response(status_code=HTTPStatus.OK, payload=None, text=None):
    mock_response = MagicMock()

    mock_response.status_code = status_code
    mock_response.ok = status_code == HTTPStatus.OK

    mock_response.json = lambda: payload
    mock_response.text = text

    return mock_response


@fixture(scope='module')
def ssl_error_expected_relay_response():
    return {
        'errors':
            [
                {
                    'code': 'unknown',
                    'message':
                        'Unable to verify SSL certificate: '
                        'Self signed certificate',
                    'type': 'fatal'
                }
            ]
    }


@fixture
def mock_exception_for_ssl_error():
    mock_response = MagicMock()
    mock_response.reason.args.__getitem__().verify_message = 'self signed' \
                                                             ' certificate'
    return mock_response


@fixture(scope='module')
def connection_error_expected_relay_response():
    return {
        'errors':
            [
                {
                    'code': 'connection error',
                    'message':
                        'Unable to connect to Exabeam, validate the '
                        'configured API endpoint: '
                        'https://exabeam.com',
                    'type': 'fatal'
                }
            ]
    }


@fixture(scope='module')
def invalid_header_error_expected_relay_response():
    return {
        'errors':
            [
                {
                    'code': 'authorization error',
                    'message':
                        'Authorization failed: wrong key',
                    'type': 'fatal'
                }
            ]
    }


@fixture(scope='module')
def bad_request_expected_relay_response():
    return {
        'errors':
            [
                {
                    'code': 'Bad Request',
                    'message': 'Unexpected response from Exabeam: '
                               'Bad request to Exabeam',
                    'type': 'fatal'
                }
            ]
    }


@fixture
def expected_exabeam_response():
    return {
        'responses': [
            {
                'took': 26,
                'timed_out': False,
                '_shards': {
                    'total': 1,
                    'successful': 1,
                    'skipped': 0,
                    'failed': 0
                },
                'hits': {
                    'total': 39963,
                    'max_score': None,
                    'hits': [
                        {
                            '_index': 'exabeam-2021.08.11',
                            '_type': 'logs',
                            '_id': 'lms.kafka.topic_10_35121_bb3b8a648af1',
                            '_score': None,
                            '_routing': 'zwt8HOYI',
                            '_source': {
                                'exa_parser_name': 'code42-file-operations-4',
                                'forwarder': 'gke-tbd2-int-e2e-standard-7c2a2d'
                                             'ba-lsxs.c.ops-dist-tbd2-int-e2e.'
                                             'internal',
                                'device_name': 'JOHNM-OFFICIAL-',
                                '@timestamp': '2021-08-11T23:09:49.462Z',
                                'device_id': '944596934062634167',
                                'file_ext': 'Executable',
                                'file_name': 'Pandora.exe',
                                'exa_adjustedEventTime': '2021-08-11T23:05:28'
                                                         '.670Z',
                                'file_size': 9.2345856E7,
                                'exa_activity_type': [
                                    'object-access/delete',
                                    'object-access'
                                ],
                                'domain': 'JOHNM-OFFICIAL-WIN10.qa.code42.com',
                                'exa_outcome': [
                                    'success'
                                ],
                                'mime': 'application/x-dosexec',
                                'accesses': 'DELETED',
                                'src_ip': '162.222.47.183',
                                'user_email': 'john.miller@c42se.com',
                                'sha256': '5fc8282e46b6e741b8d6fe2b3e35a21a62a'
                                          'f9f4368a5b94eca90f7e6d527dc6c',
                                'indexTime': '2021-08-11T23:09:49.668Z',
                                'Vendor': 'Code42',
                                'dest_host': 'JOHNM-OFFICIAL-',
                                'data_type': 'file-operations',
                                'md5': '762545aa60caa6768542e15ac96ad770',
                                'port': 4793,
                                'is_reputation_domain': False,
                                'exa_rawEventTime': '2021-08-11T23:05:28.670Z',
                                'file_path': 'C:/Program Files/WindowsApps/Pan'
                                             'doraMediaInc.29680B314EFC2_15.0.'
                                             '3.0_x64__n619g4d5j0fnw/app/',
                                'message': '<110>1 2021-08-11T23:05:28.670Z '
                                           'bb379a00ba2a Skyformation - 686537'
                                           '8086067993358 - CEF:0|Skyformation'
                                           '|SkyFormation Cloud Apps Security|'
                                           '2.0.0|sk4-resource-deleted|resourc'
                                           'e-deleted|0|cat=application-data c'
                                           's6Label=raw-event destinationServi'
                                           'ceName=Code42 fileType=file flexSt'
                                           'ring1=DELETED msg=Resource [Resour'
                                           'ce: file :: Pandora.exe] was delet'
                                           'ed by [john.miller@c42se.com] outc'
                                           'ome=Executable proto=exe requestCl'
                                           'ientApplication=Code42 - DEMO src='
                                           '162.222.47.183 suid=username suser'
                                           '=john.miller@c42se.com ext_fileCat'
                                           'egoryByExtension=Executable cs6={'
                                           '\'eventId\':\'0_c4b5e830-824a-40a3'
                                           '-a6d9-345664cfbb33_944596934062634'
                                           '167_1020014027375976393_966\'} ',
                                'file_type': 'Executable',
                                'user_uid': '920256648733700755',
                                'time': '2021-08-11T23:05:28.670Z',
                                'Product': 'Code42',
                                'file_parent': 'C:/Program Files/WindowsApps/P'
                                               'andoraMediaInc.29680B314EFC2_1'
                                               '5.0.3.0_x64__n619g4d5j0fnw/'
                                               'app/',
                                '@version': '1',
                                'exa_category': 'File',
                                'exa_device_type': [
                                    'application'
                                ],
                                'is_threat_src_ip': False,
                                'is_ransomware_src_ip': False,
                                'is_tor_src_ip': False
                            },
                            'fields': {
                                'indexTime': [
                                    '2021-08-11T23:09:49.668Z'
                                ]
                            },
                            'sort': [
                                1628723389668
                            ]
                        }
                    ]
                }
            }
        ]
    }


@fixture
def expected_relay_response(success_observe_body):
    def _make_payload(route):
        payload_to_route_match = {
            '/observe/observables': success_observe_body,
            '/refer/observables': {}
        }
        return payload_to_route_match[route]
    return _make_payload


@fixture
def success_observe_body():
    return {
        'data': {
            'sightings': {
                'count': 1,
                'docs': [
                    {
                        'confidence': 'High',
                        'count': 1,
                        'data': {
                            'columns': [
                                {
                                    'name': 'forwarder',
                                    'type': 'string'
                                },
                                {
                                    'name': 'device_name',
                                    'type': 'string'
                                },
                                {
                                    'name': 'device_id',
                                    'type': 'string'
                                },
                                {
                                    'name': 'file_ext',
                                    'type': 'string'
                                },
                                {
                                    'name': 'file_name',
                                    'type': 'string'
                                },
                                {
                                    'name': 'file_size',
                                    'type': 'string'
                                },
                                {
                                    'name': 'domain',
                                    'type': 'string'
                                },
                                {
                                    'name': 'mime',
                                    'type': 'string'
                                },
                                {
                                    'name': 'accesses',
                                    'type': 'string'
                                },
                                {
                                    'name': 'src_ip',
                                    'type': 'string'
                                },
                                {
                                    'name': 'user_email',
                                    'type': 'string'
                                },
                                {
                                    'name': 'sha256',
                                    'type': 'string'
                                },
                                {
                                    'name': 'indexTime',
                                    'type': 'string'
                                },
                                {
                                    'name': 'dest_host',
                                    'type': 'string'
                                },
                                {
                                    'name': 'data_type',
                                    'type': 'string'
                                },
                                {
                                    'name': 'md5',
                                    'type': 'string'
                                },
                                {
                                    'name': 'port',
                                    'type': 'string'
                                },
                                {
                                    'name': 'file_path',
                                    'type': 'string'
                                },
                                {
                                    'name': 'file_type',
                                    'type': 'string'
                                },
                                {
                                    'name': 'user_uid',
                                    'type': 'string'
                                },
                                {
                                    'name': 'time',
                                    'type': 'string'
                                },
                                {
                                    'name': 'file_parent',
                                    'type': 'string'
                                }
                            ],
                            'rows': [
                                [
                                    'gke-tbd2-int-e2e-standard-7c2a2dba-lsxs.c'
                                    '.ops-dist-tbd2-int-e2e.internal',
                                    'JOHNM-OFFICIAL-', '944596934062634167',
                                    'Executable', 'Pandora.exe', 92345856.0,
                                    'JOHNM-OFFICIAL-WIN10.qa.code42.com',
                                    'application/x-dosexec', 'DELETED',
                                    '162.222.47.183', 'john.miller@c42se.com',
                                    '5fc8282e46b6e741b8d6fe2b3e35a21a62af9f436'
                                    '8a5b94eca90f7e6d527dc6c',
                                    '2021-08-11T23:09:49.668Z',
                                    'JOHNM-OFFICIAL-', 'file-operations',
                                    '762545aa60caa6768542e15ac96ad770', 4793,
                                    'C:/Program Files/WindowsApps/PandoraMedia'
                                    'Inc.29680B314EFC2_15.0.3.0_x64__n619g4d5j'
                                    '0fnw/app/', 'Executable',
                                    '920256648733700755',
                                    '2021-08-11T23:05:28.670Z',
                                    'C:/Program Files/WindowsApps/PandoraMedia'
                                    'Inc.29680B314EFC2_15.0.3.0_x64__n619g4d5j'
                                    '0fnw/app/'
                                ]
                            ]
                        },
                        'description': '```\n<110>1 2021-08-11T23:05:28.670Z '
                                       'bb379a00ba2a Skyformation - 686537808'
                                       '6067993358 - CEF:0|Skyformation|SkyFo'
                                       'rmation Cloud Apps Security|2.0.0|sk4'
                                       '-resource-deleted|resource-deleted|0|'
                                       'cat=application-data cs6Label=raw-eve'
                                       'nt destinationServiceName=Code42 file'
                                       'Type=file flexString1=DELETED msg=Res'
                                       'ource [Resource: file :: Pandora.exe]'
                                       ' was deleted by [john.miller@c42se.co'
                                       'm] outcome=Executable proto=exe reque'
                                       'stClientApplication=Code42 - DEMO src'
                                       '=162.222.47.183 suid=username suser=j'
                                       'ohn.miller@c42se.com ext_fileCategory'
                                       'ByExtension=Executable cs6={\'eventId'
                                       '\':\'0_c4b5e830-824a-40a3-a6d9-345664'
                                       'cfbb33_944596934062634167_10200140273'
                                       '75976393_966\'} \n```',
                        'external_ids': [
                            'lms.kafka.topic_10_35121_bb3b8a648af1'
                        ],
                        'id': 'transient:sighting-f34e127d-a696-5e1a-8868-afa'
                              'fc4541eec',
                        'internal': True,
                        'observables': [
                            {
                                'type': 'domain', 'value': 'cisco.com'
                            }
                        ],
                        'observed_time': {
                            'start_time': '2021-08-11T23:05:28.670Z'
                        },
                        'schema_version': '1.1.7',
                        'short_description': 'Exabeam received a log from gke'
                                             '-tbd2-int-e2e-standard-7c2a2dba'
                                             '-lsxs.c.ops-dist-tbd2-int-e2e.i'
                                             'nternal containing the observab'
                                             'le',
                        'source': 'Exabeam',
                        'source_uri': 'https://exabeam.com/data/app/dataui#/d'
                                      'iscover?_g=(time:(from:now-30d))&_a=(i'
                                      'nterval:(text:Auto,val:auto),query:(qu'
                                      'ery_string:(default_field:message,quer'
                                      'y:\'_id:%22lms.kafka.topic_10_35121_bb'
                                      '3b8a648af1%22\')),queryString:\'_id:%2'
                                      '2lms.kafka.topic_10_35121_bb3b8a648af1'
                                      '%22\',searchExecuted:!t,sort:!(indexTi'
                                      'me,desc),uiState:(vis:(colors:(Count:%'
                                      '23139df2))))',
                        'title': 'Log message received by Exabeam in last 30 '
                                 'days contains observable',
                        'type': 'sighting'
                    }
                ]
            }
        }
    }
