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


@fixture(scope='module')
def unknown_response_code_relay_response():
    return {
        'errors': [
            {
                'code': 522,
                'message': 'Unexpected response from Exabeam: None',
                'type': 'fatal'
            }
        ]
    }


@fixture(scope='module')
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


@fixture(scope='module')
def expected_relay_response(success_observe_body, success_refer_body):
    def _make_payload(route):
        payload_to_route_match = {
            '/observe/observables': success_observe_body,
            '/refer/observables': success_refer_body
        }
        return payload_to_route_match[route]
    return _make_payload


@fixture(scope='module')
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
                        'source_uri': 'https://exabeam.com/data/app/dataui#/di'
                                      'scover?_g=(time:(from:now-30d))&_a=(int'
                                      'erval:(text:Auto,val:auto),query:(query'
                                      '_string:(default_field:message,query:\''
                                      '_id:%22lms.kafka.topic_10_35121_bb3b8a6'
                                      '48af1%22\')),queryString:\'_id:%22lms.k'
                                      'afka.topic_10_35121_bb3b8a648af1%22\',s'
                                      'earchExecuted:!t,sort:!(indexTime,desc)'
                                      ',uiState:(vis:(colors:(Count:%23139df2)'
                                      ')))',
                        'title': 'Log message received by Exabeam in last 30 '
                                 'days contains observable',
                        'type': 'sighting'
                    }
                ]
            }
        }
    }


@fixture(scope='module')
def success_refer_body():
    return {
        'data':
            [
                {
                    'categories':
                        [
                            'Search',
                            'Exabeam'
                        ],
                    'description': 'Search for this domain in '
                                   'Exabeam Data Lake',
                    'id': 'ref-exabeam-search-domain-cisco.com',
                    'title': 'Search for this domain',
                    'url': 'https://exabeam.com/data/app/dataui#/discover?_g=('
                           'time:(from:now-30d))&_a=(interval:(text:Auto,val:a'
                           'uto),query:(query_string:(default_field:message,qu'
                           'ery:\'%22cisco.com%22%20AND%20NOT%20(event_sub'
                           'type:%22Exabeam%20Audit%20Event%22)\')),queryStrin'
                           'g:\'%22cisco.com%22%20AND%20NOT%20(event_subty'
                           'pe:%22Exabeam%20Audit%20Event%22)\',searchExecuted'
                           ':!t,sort:!(indexTime,desc),uiState:(vis:(colors:(C'
                           'ount:%23139df2))))'
                }
            ]
    }


def exabeam_response_tile(tile_id):
    tile_id_map = {
        'affected_ips': exabeam_response_affected_ips(),
        'activity_types': exabeam_response_activity_types()
    }
    return tile_id_map[tile_id]


def exabeam_response_affected_ips():
    return {
        'aggregations': {
            'is_threat_src_ip': {
                'doc_count_error_upper_bound': 0,
                'sum_other_doc_count': 0,
                'buckets': [
                    {
                        'key': 0,
                        'key_as_string': 'false',
                        'doc_count': 495736
                    }
                ]
            },
            'is_ransomware_src_ip': {
                'doc_count_error_upper_bound': 0,
                'sum_other_doc_count': 0,
                'buckets': [
                    {
                        'key': 0,
                        'key_as_string': 'false',
                        'doc_count': 495736
                    }
                ]
            },
            'is_tor_src_ip': {
                'doc_count_error_upper_bound': 0,
                'sum_other_doc_count': 0,
                'buckets': [
                    {
                        'key': 0,
                        'key_as_string': 'false',
                        'doc_count': 495736
                    }
                ]
            }
        }
    }


def exabeam_response_activity_types():
    return {
        'aggregations': {
            'exa_activity_type.keyword': {
                'doc_count_error_upper_bound': 0,
                'sum_other_doc_count': 0,
                "buckets": [
                    {
                        'key': 'object-access',
                        'doc_count': 303061
                    },
                    {
                        'key': 'object-access/write',
                        'doc_count': 156235
                    },
                    {
                        'key': 'object-access/delete',
                        'doc_count': 146194
                    }
                ]
            }
        }
    }


def relay_response_tile_data(tile_id):
    tile_id_map = {
        'affected_ips': relay_response_affected_ips(),
        'activity_types': relay_response_activity_types()
    }
    return tile_id_map[tile_id]


def relay_response_affected_ips():
    return [
        {
            'icon': 'warning',
            'label': 'Ransomware IPs',
            'link_uri': 'https://exabeam.com/data/app/dataui#/discover?_g=(ti'
                        'me:(from:now-30d))&_a=(interval:(text:Auto,val:auto)'
                        ',query:(query_string:(default_field:message,query:\''
                        'is_ransomware_src_ip:"true"%20AND%20NOT%20(event_sub'
                        'type:%22Exabeam%20Audit%20Event%22)\')),queryString:'
                        '\'is_ransomware_src_ip:"true"%20AND%20NOT%20(event_s'
                        'ubtype:%22Exabeam%20Audit%20Event%22)\',searchExecut'
                        'ed:!t,sort:!(indexTime,desc),uiState:(vis:(colors:(C'
                        'ount:%23139df2))))',
            'value': 0,
            'value_unit': 'integer'
        },
        {
            'icon': 'warning',
            'label': 'Threat IPs',
            'link_uri': 'https://exabeam.com/data/app/dataui#/discover?_g=(ti'
                        'me:(from:now-30d))&_a=(interval:(text:Auto,val:auto)'
                        ',query:(query_string:(default_field:message,query:\''
                        'is_threat_src_ip:"true"%20AND%20NOT%20(event_subtype'
                        ':%22Exabeam%20Audit%20Event%22)\')),queryString:\'is'
                        '_threat_src_ip:"true"%20AND%20NOT%20(event_subtype:%'
                        '22Exabeam%20Audit%20Event%22)\',searchExecuted:!t,so'
                        'rt:!(indexTime,desc),uiState:(vis:(colors:(Count:%23'
                        '139df2))))',
            'value': 0,
            'value_unit': 'integer'
        },
        {
            'icon': 'warning',
            'label': 'Tor IPs',
            'link_uri': 'https://exabeam.com/data/app/dataui#/discover?_g=(ti'
                        'me:(from:now-30d))&_a=(interval:(text:Auto,val:auto)'
                        ',query:(query_string:(default_field:message,query:\''
                        'is_tor_src_ip:"true"%20AND%20NOT%20(event_subtype:%2'
                        '2Exabeam%20Audit%20Event%22)\')),queryString:\'is_to'
                        'r_src_ip:"true"%20AND%20NOT%20(event_subtype:%22Exab'
                        'eam%20Audit%20Event%22)\',searchExecuted:!t,sort:!(i'
                        'ndexTime,desc),uiState:(vis:(colors:(Count:%23139df2'
                        '))))',
            'value': 0,
            'value_unit': 'integer'
        }
    ]


def relay_response_activity_types():
    return [
        {'key': 0,
         'link_uri': 'https://exabeam.com/data/app/dataui#/discover?_g=(time:('
                     'from:now-30d))&_a=(interval:(text:Auto,val:auto),query:('
                     'query_string:(default_field:message,query:\'object-acces'
                     's:"true"%20AND%20NOT%20(event_subtype:%22Exabeam%20Audit'
                     '%20Event%22)\')),queryString:\'object-access:"true"%20AN'
                     'D%20NOT%20(event_subtype:%22Exabeam%20Audit%20Event%22)'
                     '\',searchExecuted:!t,sort:!(indexTime,desc),uiState:(vis'
                     ':(colors:(Count:%23139df2))))',
         'value': 303061
         },
        {
            'key': 1,
            'link_uri': 'https://exabeam.com/data/app/dataui#/discover?_g=(ti'
                        'me:(from:now-30d))&_a=(interval:(text:Auto,val:auto)'
                        ',query:(query_string:(default_field:message,query:\''
                        'object-access/write:"true"%20AND%20NOT%20(event_subt'
                        'ype:%22Exabeam%20Audit%20Event%22)\')),queryString:'
                        '\'object-access/write:"true"%20AND%20NOT%20(event_su'
                        'btype:%22Exabeam%20Audit%20Event%22)\',searchExecute'
                        'd:!t,sort:!(indexTime,desc),uiState:(vis:(colors:(Co'
                        'unt:%23139df2))))',
            'value': 156235
        },
        {
            'key': 2,
            'link_uri': 'https://exabeam.com/data/app/dataui#/discover?_g=(ti'
                        'me:(from:now-30d))&_a=(interval:(text:Auto,val:auto)'
                        ',query:(query_string:(default_field:message,query:\''
                        'object-access/delete:"true"%20AND%20NOT%20(event_sub'
                        'type:%22Exabeam%20Audit%20Event%22)\')),queryString:'
                        '\'object-access/delete:"true"%20AND%20NOT%20(event_s'
                        'ubtype:%22Exabeam%20Audit%20Event%22)\',searchExecut'
                        'ed:!t,sort:!(indexTime,desc),uiState:(vis:(colors:(C'
                        'ount:%23139df2))))',
            'value': 146194
        }
    ]


def relay_response_tiles():
    return {
        'data': [affected_ips_tile(),
                 activity_types_tile()]
    }


def relay_response_tiles_tile():
    return {
        'data': affected_ips_tile()
    }


def affected_ips_tile():
    return {
        'description': 'Affected IPs chart shows how many IPs are '
                       'ransomware, threat or tor',
        'id': 'affected_ips',
        'periods': ['last_30_days'],
        'short_description': 'Affected IPs found in Exabeam Data Lake',
        'tags': ['affected_ips'],
        'title': 'Affected IPs',
        'type': 'metric_group'
    }


def activity_types_tile():
    return {
        'description': 'Activity types chart shows distribution of events '
                       'that triggered log creation by its types.',
        'id': 'activity_types',
        'periods': ['last_30_days'],
        'short_description': 'Activity types found in Exabeam Data Lake',
        'tags': ['activity_types'],
        'title': 'Activity Types',
        'type': 'donut_graph'
    }
