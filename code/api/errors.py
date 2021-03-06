from http import HTTPStatus


AUTH_ERROR = 'authorization error'
INVALID_ARGUMENT = 'invalid argument'
UNKNOWN = 'unknown'
CONNECTION_ERROR = 'connection error'
INVALID_HOST = 'Invalid host'
EXABEAM_DOWN = 'Exabeam is down'


class TRFormattedError(Exception):
    def __init__(self, code, message, type_='fatal'):
        super().__init__()
        self.code = code or UNKNOWN
        self.message = message or 'Something went wrong.'
        self.type_ = type_

    @property
    def json(self):
        return {'type': self.type_,
                'code': self.code,
                'message': self.message}


class AuthorizationError(TRFormattedError):
    def __init__(self, message):
        super().__init__(
            AUTH_ERROR,
            f'Authorization failed: {message}'
        )


class InvalidArgumentError(TRFormattedError):
    def __init__(self, message):
        super().__init__(
            INVALID_ARGUMENT,
            str(message)
        )


class WatchdogError(TRFormattedError):
    def __init__(self):
        super().__init__(
            code='health check failed',
            message='Invalid Health Check'
        )


class ExabeamSSLError(TRFormattedError):
    def __init__(self, error):
        error = error.args[0].reason.args[0]
        message = getattr(error, 'verify_message', error.args[0]).capitalize()
        super().__init__(
            UNKNOWN,
            f'Unable to verify SSL certificate: {message}'
        )


class ExabeamConnectionError(TRFormattedError):
    def __init__(self, url):
        super().__init__(
            CONNECTION_ERROR,
            'Unable to connect to Exabeam,'
            f' validate the configured API endpoint: {url}'
        )


class CriticalExabeamResponseError(TRFormattedError):
    def __init__(self, response):
        status_phrase_map = {
            530: INVALID_HOST,
            522: EXABEAM_DOWN
        }
        connection_error_statuses = (530, 522,)
        # This try except section is needed because
        # Exabeam can return not standard 522, 530 status codes
        try:
            code = HTTPStatus(response.status_code).phrase
        except ValueError:
            code = (CONNECTION_ERROR
                    if response.status_code in connection_error_statuses
                    else str(response.status_code))

        super().__init__(
            code,
            'Unexpected response from Exabeam: '
            f'{status_phrase_map.get(response.status_code, response.text)}'
        )


class MoreMessagesAvailableWarning(TRFormattedError):
    def __init__(self, observable):
        super().__init__(
            'too-many-messages-warning',
            f'There are more messages in Exabeam for {observable}'
            ' than can be displayed in Threat Response. Login to the '
            'Exabeam console to see all messages.',
            type_='warning'
        )
