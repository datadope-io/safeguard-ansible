import collections

from pysafeguard import *

CredentialPlugin = collections.namedtuple('CredentialPlugin', ['name', 'inputs', 'backend'])

def _get_spp_credential(**kwargs):
    """Retrieve the credential that corresponds to the API key
        :arg appliance: SPP appliance to connection with
        :arg api_key: Api key that coresponds to a credential
        :arg cert: Client authentication certificate
        :arg key: Client authentication key
        :arg tls_cert: tls certificate or False
        :arg a2atype: A2a credential type
        :returns: a text string containing the credential
    """

    api_key = kwargs.get('spp_api_key', None)
    appliance = kwargs.get('spp_appliance', None)
    cert = kwargs.get('spp_certificate_path', None)
    key = kwargs.get('spp_key_path', None)
    tls_cert = kwargs.get('spp_tls_path', False)
    credential_type = kwargs.get('spp_credential_type', A2ATypes.PASSWORD)
    if credential_type.lower() == A2ATypes.PASSWORD:
        credential_type = A2ATypes.PASSWORD
    elif credential_type.lower() == A2ATypes.PRIVATEKEY:
        credential_type = A2ATypes.PRIVATEKEY
    else:
        raise AnsibleError('Invalid credential type: ' + credential_type)

    if not api_key:
        raise ValueError('Missing credential API key.')
    if not appliance:
        raise ValueError('Missing appliance IP address or host name.')
    if not cert:
        raise ValueError('Missing client authentication certificate path.')
    if not key:
        raise ValueError('Missing client authentication key path.')

    try:
        return PySafeguardConnection.a2a_get_credential(appliance, api_key, cert, key, tls_cert, a2aType=credential_type)
    except Exception as e:
        print(e)
        raise ValueError('Failed to retrieve the credential.')


spp_plugin = CredentialPlugin(
    'Safeguard Credential',
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
        }, {
            'id': 'spp_tls_path',
            'label': 'Safeguard TLS certificate file path',
            'type': 'string',
        }, {
            'id': 'spp_credential_type',
            'label': 'Safeguard credential type to retrieve',
            'type': 'string',
            'choices': ['password', 'privatekey']
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


