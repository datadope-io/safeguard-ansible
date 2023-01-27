# (c) 2023, Brad Nicholes <brad.nicholes@oneidentity.com>
# (c) 2023, One Identity LLC.

from __future__ import (absolute_import, division, print_function)
from os.path import dirname
import sys
from ansible.plugins.lookup import LookupBase
from ansible.module_utils._text import to_bytes, to_native, to_text
from ansible.errors import AnsibleError, AnsibleAssertionError
__metaclass__ = type

DOCUMENTATION = """
    name: safeguardcredentials
    version_added: "0.9"
    author:
      - Brad Nicholes (!UNKNOWN) <brad.nicholes@oneidentity.com>
    short_description: retrieve credentials from Safeguard for Privileged Passwords vault
    description:
      - Retrieve credentials from the Safeguard for Privileged Passwords vault given a user certificate and API key that
        corresponds to a specific credential.
    options:
      _terms:
        description:
          - List of API keys that correspond to retrievable credentials
        required: True
      a2aconnection:
        description:
          - Safeguard for Privileged Passwords appliance connection information
          - The a2aconnection must contain the following properties
            - spp_appliance - IP address or host name of the Safeguard for Prvileged Passwords appliance
            - spp_certificate_file - Full path to the A2A client authentication certificate
            - spp_certificate_key - Full path to the A2A client authentication private key
            - spp_tls_cert(optional) - Full path to the TLS publis certificate that is associated with the SPP appliance
        required: True
    notes:
      - Please see the configuration for the Safeguard for Privileged Passwords Application to Application registration.
      - Each credential that is retrieved from Safeguard for Privileged Passwords will have an identifying API key.
      - The safeguardcredentials lookup plugin requires OneIdentity PySafeguard module.  Please see https://github.com/OneIdentity/PySafeguard
"""

EXAMPLES = """
  vars:
    spp_credential_apikey: safyBECB8SW5g0Udk7GRFh6LaQ/KoI0eNOW4JK8Cqeo=
    a2aconnection:
      spp_appliance: 192.168.0.1
      spp_certificate_file: /etc/ansible/certs/CN=a2ausercert.pem
      spp_certificate_key: /etc/ansible/certs/CN=a2ausercert.key
      spp_tls_cert_key: /etc/ansible/certs/spptlscert.pem
  name: retrieve a credential
    ansible.builtin.set_fact:
      password: "{{ lookup('safeguardcredentials', spp_credential_apikey, a2aconnection) }}"

"""

RETURN = """
_raw:
  description:
    - a credential
  type: list
  elements: str
"""

from ansible.errors import AnsibleError, AnsibleAssertionError
from ansible.module_utils._text import to_bytes, to_native, to_text
from ansible.plugins.lookup import LookupBase

import sys
from os.path import dirname
sys.path.append(dirname(__file__))

from pysafeguard import *

def _get_spp_credential(appliance, api_key, certificate_file, certificate_key, tls_cert):
    """Retrieve the credential that corresponds to the API key
      :arg appliance: SPP appliance to connection with
      :arg api_key: Api key that coresponds to a credential
      :arg certificate_file: Client authentication certificate
      :arg certificate_key: Client authentication key
      :arg tls_cert: tls certificate or False
      :returns: a text string containing the credential
    """

    try:
        password = PySafeguardConnection.a2a_get_credential(appliance, api_key, certificate_file, certificate_key, tls_cert)
    except Exception as e:
        raise AnsibleError('Failed to retrieve the credential: %s' % to_native(e))

    return password


class LookupModule(LookupBase):

    def run(self, terms, variables, **kwargs):
        ret = []

        self.set_options(var_options=variables, direct=kwargs)

        a2aconnection = self.get_option('a2aconnection')

        appliance = a2aconnection.get('spp_appliance', None)
        cert = a2aconnection.get('spp_certificate_file', None)
        key = a2aconnection.get('spp_certificate_key', None)
        tls_cert = a2aconnection.get('spp_tls_cert', False)

        if not appliance:
            raise AnsibleError('Missing appliance IP address or host name.')
        if not cert:
            raise AnsibleError('Missing client authentication certificate path.')
        if not key:
            raise AnsibleError('Missing client authentication key path.')

        for term in terms:
            pw = _get_spp_credential(appliance, term, cert, key, tls_cert)
            ret.append(pw)

        return ret
