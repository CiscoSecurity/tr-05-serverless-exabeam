import json


class Config:
    settings = json.load(open('container_settings.json', 'r'))
    VERSION = settings['VERSION']

    USER_AGENT = ('SecureX Threat Response Integrations '
                  '<tr-integrations-support@cisco.com>')
    CTR_ENTITIES_LIMIT_DEFAULT = 100

    EXABEAM_API_ENDPOINT = 'https://{host}'

    HUMAN_READABLE_OBSERVABLE_TYPES = {
        'certificate_common_name': 'certificate common name',
        'certificate_issuer': 'certificate issuer',
        'certificate_serial': 'certificate serial',
        'cisco_mid': 'Cisco message ID',
        'cisco_uc_id': 'Cisco UC ID',
        'device': 'device',
        'domain': 'domain',
        'email': 'email',
        'email_messageid': 'email message ID',
        'email_subject': 'email subject',
        'file_name': 'file name',
        'file_path': 'file path',
        'hostname': 'hostname',
        'imei': 'IMEI',
        'imsi': 'IMSI',
        'ip': 'IP',
        'ipv6': 'IPv6',
        'mac_address': 'MAC address',
        'md5': 'MD5',
        'ms_machine_id': 'Microsoft machine ID',
        'mutex': 'mutex',
        'ngfw_id': 'NGFW ID',
        'ngfw_name': 'NGFW name',
        'odns_identity': 'ODNS identity',
        'odns_identity_label': 'ODNS identity label',
        'orbital_node_id': 'Orbital node ID',
        'pki_serial': 'PKI serial',
        'process_name': 'process name',
        'registry_key': 'registry key',
        'registry_name': 'registry name',
        'registry_path': 'registry path',
        's1_agent_id': 'SentinelOne agent ID',
        'sha1': 'SHA1',
        'sha256': 'SHA256',
        'swc_device_id': 'SWC device ID',
        'url': 'URL',
        'user': 'user',
        'user_agent': 'user agent',
    }

    URL_PARAMS_FOR_SIGHTING = '_g=(time:(from:now-30d))&_a=(interval:(text:' \
                              'Auto,val:auto),query:(query_string:(default_' \
                              'field:message,query:\'_id:%22{value}%22\')),' \
                              'queryString:\'_id:%22{value}%22\',searchExec' \
                              'uted:!t,sort:!(indexTime,desc),uiState:(vis:' \
                              '(colors:(Count:%23139df2))))'

    URL_PARAMS_FOR_REFER = '_g=(time:(from:now-30d))&_a=(interval:(text:Aut' \
                           'o,val:auto),query:(query_string:(default_field:' \
                           'message,query:\'%22{value}%22%20AND%20NOT%20(ev' \
                           'ent_subtype:%22Exabeam%20Audit%20Event%22)\')),' \
                           'queryString:\'%22{value}%22%20AND%20NOT%20(even' \
                           't_subtype:%22Exabeam%20Audit%20Event%22)\',sear' \
                           'chExecuted:!t,sort:!(indexTime,desc),uiState:(v' \
                           'is:(colors:(Count:%23139df2))))'

    URL_PARAMS_FOR_TILE = '_g=(time:(from:now-30d))&_a=(interval:(text:Auto' \
                          ',val:auto),query:(query_string:(default_field:me' \
                          'ssage,query:\'{value}%20AND%20NOT%20(event_subty' \
                          'pe:%22Exabeam%20Audit%20Event%22)\')),queryStrin' \
                          'g:\'{value}%20AND%20NOT%20(event_subtype:%22Exab' \
                          'eam%20Audit%20Event%22)\',searchExecuted:!t,sort' \
                          ':!(indexTime,desc),uiState:(vis:(colors:(Count:%' \
                          '23139df2))))'

    TILE_PERIODS_MAP = {
        'last_24_hours': 1,
        'last_7_days': 7,
        'last_30_days': 30
    }
