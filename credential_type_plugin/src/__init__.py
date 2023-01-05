import collections

from pysafeguard import *

CredentialPlugin = collections.namedtuple('CredentialPlugin', ['name', 'inputs', 'backend'])

def _get_spp_credential(**kwargs):
    """Retrieve the credential that corresponds to the API key
        :arg appliance: SPP appliance to connection with
        :arg api_key: Api key that coresponds to a credential
        :arg cert: Client authentication certificate
        :arg key: Client authentication key
        :returns: a text string containing the credential
    """

    api_key = kwargs.get('spp_api_key')
    appliance = kwargs.get('spp_appliance')
    cert = kwargs.get('spp_certificate_path')
    key = kwargs.get('spp_key_path')

    if not api_key:
        raise ValueError('Missing credential API key.')
    if not appliance:
        raise ValueError('Missing appliance IP address or host name.')
    if not cert:
        raise ValueError('Missing client authentication certificate path.')
    if not key:
        raise ValueError('Missing client authentication key path.')

    try:
        return PySafeguardConnection.a2a_get_credential(appliance, api_key, cert, key, False)
    except Exception as e:
        print(e)
        raise ValueError('Failed to retrieve the credential.')


spp_plugin = CredentialPlugin(
    'SPP Credential Plugin',
    inputs={
        'fields': [{
            'id': 'spp_api_key',
            'label': 'Safeguard Credential API key',
            'type': 'string',
        }, {
            'id': 'spp_appliance',
            'label': 'Safeguard Appliance IP or Host name',
            'type': 'string',
        }, {
            'id': 'spp_certificate_path',
            'label': 'Safeguard client certificate file path',
            'type': 'string',
        }, {
            'id': 'spp_key_path',
            'label': 'Safeguard client key file path',
            'type': 'string',
        }],
        'metadata': [],
        'required': ['spp_api_key', 'spp_appliance', 'spp_certificate_path', 'spp_key_path'],
    },
    # backend is a callable function which will be passed all of the values
    # defined in `inputs`; this function is responsible for taking the arguments,
    # interacting with the third party credential management system in question
    # using Python code, and returning the value from the third party
    # credential management system
    backend = _get_spp_credential
)


