from datetime import datetime, timedelta

from flask import current_app
import requests
from requests.exceptions import (
    SSLError,
    ConnectionError,
    MissingSchema,
    InvalidSchema,
    InvalidURL,
    InvalidHeader
)

from api.errors import (
    AuthorizationError,
    ExabeamSSLError,
    ExabeamConnectionError,
    CriticalExabeamResponseError,
    MoreMessagesAvailableWarning
)
from api.utils import add_error


INVALID_CREDENTIALS = 'wrong key'


class ExabeamClient:
    def __init__(self, key):
        self._headers = {
            'ExaAuthToken': key,
            'User-Agent': current_app.config['USER_AGENT']
        }
        self._entities_limit = current_app.config['CTR_ENTITIES_LIMIT']
        self._entities_limit_default = current_app.config[
            'CTR_ENTITIES_LIMIT_DEFAULT']

    @property
    def _url(self):
        url = current_app.config['EXABEAM_API_ENDPOINT']
        return url.format(host=current_app.config['HOST'])

    def health(self):
        return self._request(path='api/auth/check')

    def _request(self, path, method='GET', body=None,
                 params=None, data_extractor=lambda r: r.json()):
        url = '/'.join([self._url, path])

        try:
            response = requests.request(method, url, json=body,
                                        params=params, headers=self._headers)
        except SSLError as error:
            raise ExabeamSSLError(error)
        except (ConnectionError, MissingSchema, InvalidSchema, InvalidURL):
            raise ExabeamConnectionError(self._url)
        except (UnicodeEncodeError, InvalidHeader):
            raise AuthorizationError(INVALID_CREDENTIALS)

        if response.ok:
            return data_extractor(response)

        raise CriticalExabeamResponseError(response)

    @staticmethod
    def _get_payload(indices, observable):
        return {
            'clusterWithIndices': [
                {
                    'clusterName': 'local',
                    'indices': indices
                }
            ],
            'query': f'"{observable}" AND NOT (event_subtype:'
                     '"Exabeam Audit Event")',
            'size': 101,
            'sortBy': [
                {
                    'field': 'indexTime',
                    'order': 'desc'
                }
            ]
        }

    def get_data(self, observable):
        today = datetime.today()
        indices = []
        for days in range(1, 31):
            delta = timedelta(days=days)
            indices.append(f'exabeam-{(today - delta).strftime("%Y.%m.%d")}')
        response = self._request(path='dl/api/es/search',
                                 method='POST',
                                 body=self._get_payload(indices, observable))
        hits = response['responses'][0]['hits']['hits']
        if len(hits) > self._entities_limit_default:
            add_error(MoreMessagesAvailableWarning(observable))
        return hits[:self._entities_limit]
