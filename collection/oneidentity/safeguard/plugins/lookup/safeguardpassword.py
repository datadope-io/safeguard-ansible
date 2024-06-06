# (c) 2024, Adrian Lopez <adrian.lopez@datadope.io>
# (c) 2024, Datadope

from __future__ import (absolute_import, division, print_function)
from os.path import dirname
import sys
from ansible.plugins.lookup import LookupBase
from ansible.errors import AnsibleError
__metaclass__ = type

DOCUMENTATION = """
    name: safeguardpassword
    version_added: "0.9"
    author:
      - Adrian Lopez (Datadope) <adrian.lopez@datadope.io>
    short_description: retrieve asset password from Safeguard for Privileged Passwords vault
    description:
      - Retrieve asset access password from the Safeguard for Privileged Passwords vault given a username and password
        to authenticate to the Safeguard appliance.
    options:
      _terms:
        description:
          - Asset name to get the password for
        type: str
        required: True
      appliance:
        description: Safeguard for Privileged Passwords appliance IP address or host name
        type: str
        required: True
      username:
        description: Authentication user name.
        type: str
        required: True
      password:
        description: Authentication password.
        type: str
        required: True
    notes:
      - The safeguardcredentials lookup plugin requires OneIdentity PySafeguard module.  Please see https://github.com/OneIdentity/PySafeguard
"""

EXAMPLES = """
  vars:
    spp_appliance: 192.168.0.1
    spp_username: foo
    spp_password: mysecret
  name: retrieve a password
    ansible.builtin.set_fact:
      password: "{{ lookup('safeguardpassword', 'myasset', appliance=spp_appliance, username=spp_username, password=spp_password) }}"
"""

RETURN = """
_raw:
  description:
    - the password for the entitlement
  type: list
  type: str
"""

from ansible.plugins.lookup import LookupBase
from ansible.utils.display import Display

display = Display()

import sys
from os.path import dirname
sys.path.append(dirname(__file__))

from pysafeguard import PySafeguardConnection, HttpMethods, Services
from tenacity import retry, retry_if_exception_type, stop_after_attempt


class LookupModule(LookupBase):

    def run(self, terms, variables=None, **kwargs):
        ret = []

        self.set_options(var_options=variables, direct=kwargs)

        username = self.get_option('username', None)
        password = self.get_option('password', None)
        appliance = self.get_option('appliance', None)


        try:
            display.vvvv("Connecting to Safeguard '%s' as '%s' to request password for asset '%s'" % (appliance, username, terms[0]))
            self.connection = PySafeguardConnection(appliance, verify=False)
            self.connection.connect_password(username, password)
        except Exception as e:
            raise AnsibleError(f"Error connecting to Safeguard: {e}")

        try:
            ret = [self.get_password(asset_name=terms[0])]
        except Exception as e:
            raise AnsibleError(f"Error obtaining password: {e}")

        return ret

    def existing_request(self, asset_name):
        result = self.connection.invoke(HttpMethods.GET, Services.CORE, "AccessRequests",
                                   query={"q": asset_name})
        if result.status_code != 200:
            raise AnsibleError(f"Error obtaining access requests: {result.status_code} - {result.text}")

        request = result.json()
        # If lenght is 0, there is no request, raise exception
        if len(request) == 0:
            raise AnsibleError(f"Access request not found for '{asset_name}', but it should exist")
        elif len(request) == 1:
            return request[0]["Id"]

        # Iterate over the requests and return the first one that matches the server name, its not expired and in a state that allows password checkout
        display.vvvv("Multiple access requests found for '%s', checking for the one that matches the asset name and is not expired" % asset_name)
        for r in request:
            if r["AccountAssetName"] == asset_name and \
                    not r["WasExpired"] and \
                    ( r["State"] == "RequestAvailable" or \
                        r["State"] == "PasswordCheckedOut" ):

                return r["Id"]

        raise AnsibleError(f"Multiple access requests found for '{asset_name}', but no one matches the server name or is not expired")


    @retry(retry=retry_if_exception_type(AnsibleError), stop=stop_after_attempt(2))
    def get_password(self, asset_name):
        # Use query to get the entitlements matching server
        result = self.connection.invoke(HttpMethods.GET, Services.CORE, "Me/RequestEntitlements",
                                   query={
                                       # AssetName filter always return an empty list
                                       "q": asset_name,
                                       "accessRequestType": "Password",
                                   }
        )

        if result.status_code != 200:
            raise AnsibleError(f"Error obtaining entitlements: {result.status_code} - {result.text}")

        entitlements = result.json()

        # Filter to get the exact match. Match by name or network address. Ignore case.
        asset = list(x for x in entitlements if x.get('Account', {}).get('AssetName').lower() == asset_name.lower() or x.get('Account', {}).get('AssetNetworkAddress').lower() == asset_name.lower())

        if not asset:
            raise AnsibleError(f"Asset with name '{asset_name}' not found")
        elif len(asset) > 1:
            raise AnsibleError(f"Multiple entitlements found for '{asset_name}': {asset}")

        asset = asset[0]

        # Create a request for a password
        account_id = asset["Account"]["Id"]
        asset_id = asset["Account"]["AssetId"]
        result = self.connection.invoke(HttpMethods.POST, Services.CORE, "AccessRequests",
                                   body={
                                        "AccountId": account_id,
                                        "AssetId": asset_id,
                                        "AccessRequestType": "Password",
                                        "ReasonComment": f"Ansible lookup plugin request for asset '{asset_name}'",
                                        })

        # if error 400, the password is already requested, get the request id
        if result.status_code == 400 and "You already have a request for the account" in result.text:
            display.vvvv(f"Access request already exists for '{asset_name}'")
            request_id = self.existing_request(asset_name)
        elif result.status_code != 201:
            raise AnsibleError(f"Error creating access request: {result.status_code} - {result.text}")
        else:
            request_id = result.json()["Id"]

        # Get the password
        result = self.connection.invoke(HttpMethods.POST, Services.CORE, f"AccessRequests/{request_id}/CheckOutPassword")

        if result.status_code != 200:
            raise AnsibleError(f"Error checking out password: {result.status_code} - {result.text}")

        return result.json()
