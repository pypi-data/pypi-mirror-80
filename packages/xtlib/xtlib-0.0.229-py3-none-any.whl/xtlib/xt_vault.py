#
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT license.
#
# xt_vault.py: retreives secrets from the xt vault services
''' 
it works!  "no device code" authentication in browser, just like Azure Portal and CLI.
'''
import os
import json
import time

from xtlib import utils
from xtlib import errors
from xtlib import console
from xtlib import pc_utils
from xtlib import constants
from xtlib import file_utils
from xtlib.cache_client import CacheClient

class XTVault():

    def __init__(self, vault_url, store_name, secret_name):
        self.vault_url = vault_url
        self.store_name = store_name
        self.client = None
        self.authentication = None
        self.keys = None
        self.secret_name = secret_name

    def init_creds(self, authentication):
        cache_client = CacheClient()
        loaded = False
        self.authentication = authentication

        #utils.debug_break()

        loaded = self._load_grok_creds()
        if not loaded:
            loaded = self._load_node_creds()
        if not loaded and self.vault_url:
            # normal XT client
            creds = cache_client.get_creds(self.store_name)
            if creds:
                self.apply_creds(creds)
            else:
                creds = self._get_creds_from_login(authentication, reason="cache not set")
                cache_client.store_creds(self.store_name, creds)

    def _load_grok_creds(self):
        fn_keys = "keys.bin"
        loaded = False

        if not os.path.exists(fn_keys):
            fn_keys = os.path.expanduser("~/.xt/stores/{}/keys.bin".format(self.store_name))

        if os.path.exists(fn_keys):
            # GROK server creds
            creds = file_utils.read_text_file(fn_keys)  
            self.apply_creds(creds)

            fn_cert = os.path.join(os.path.dirname(fn_keys), "xt_cert.pem")
            if os.path.exists(fn_cert):
                cert = file_utils.read_text_file(fn_keys) 
                self.keys["xt_server_cert"] = cert

            console.diag("init_creds: using grok server 'keys.bin' file")
            loaded = True

        return loaded

    def _load_node_creds(self):
        loaded = False

        store, mongo = get_store_and_mongo_creds_on_compute_node()
        if store:
            # creds are limited in this case to just Store access [storage + mongo]
            kv = {}
            if store:
                kv[store["name"]] = store["key"]

            if mongo:
                kv[mongo["name"]] = mongo["key"]

            creds = json.dumps(kv)
            self.apply_creds(creds)

            console.print("init_creds: using compute node ENV VAR settings: {}".format(dd))
            loaded = True

        return loaded

    def _get_creds_from_login(self, authentication, reason=None):

        # use normal Key Value
        from azure.keyvault.secrets import SecretClient

        if authentication == "auto":
            authentication = "browser" if pc_utils.has_gui() else "device-code"

        if authentication == "browser":
            console.print("authenticating with azure thru browser... ", flush=True, end="")
            from azure.identity import InteractiveBrowserCredential
            credential = InteractiveBrowserCredential()  
        elif authentication == "device-code":
            # console.print("authenticating with azure thru device code... ", flush=True, end="")
            from azure.identity import DeviceCodeCredential
            from azure.identity._constants import AZURE_CLI_CLIENT_ID 

            console.print("using device-code authorization (Azure AD currently requires 2-4 authenications here)")
            credential = DeviceCodeCredential(client_id=AZURE_CLI_CLIENT_ID)  
        else:
            errors.syntax_error("unrecognized authentication type '{}'".format(authentication))

        new_creds = True
        outer_token = credential.get_token()
        token = outer_token.token

        # expires = outer_token[1]
        # elapsed = expires - time.time()
        #print(" [new token expires in {:.2f} mins] ".format(elapsed/60), end="")

        # get keys from keyvault
        self.client = SecretClient(self.vault_url, credential=credential)
        key_text = self.get_secret_live(self.secret_name)
        console.print("authenticated successfully", flush=True)

        #xt_client_cert = self.get_secret_live("xt-clientcert")
        xt_server_cert = self.get_secret_live("xt-servercert")

        # write all our creds to self.keys
        self.apply_creds(key_text)
        self.keys["xt_server_cert"] = xt_server_cert

        self.keys["object_id"] = self.get_me_graph_property(token, "id")

        # return creds as json string
        return json.dumps(self.keys)

    def apply_creds(self, creds_text):
        try:
            self.keys = json.loads(creds_text)
        except BaseException as ex:
            msg = "Error in parsing vault secret '{}' as JSON string: {}".format(self.secret_name, ex)
            errors.general_error(msg)

    def get_secret(self, id):
        # returned cached copy (only ever needs 1 roundtrip)
        if self.keys:
            if not id in self.keys:
                errors.creds_error("Missing key in memory vault: {}".format(id), show_stack=True)

            return self.keys[id]

        return None

    def get_secret_live(self, id):
        secret_bundle = self.client.get_secret(id)
        secret = secret_bundle.value
        return secret

    def get_me_graph_property(self, token, property_name):
        #console.print("get_user_principle_name: token=", token)

        import requests
        import json

        endpoint =  "https://graph.microsoft.com/v1.0/me"
        headers = {'Authorization': 'Bearer ' + token}

        graph_data = requests.get(endpoint, headers=headers).json()
        if "error" in graph_data:
            error = graph_data["error"]
            errors.config_error("{}: {}".format(error["code"], error["message"]))

        #console.print("get_user_principle_name: graph_data=", graph_data)

        upn = graph_data[property_name]
        return upn

# flat functions
def get_store_and_mongo_creds_on_compute_node():

    sd = None
    md = None

    sc = os.getenv("XT_STORE_CREDS")
    sc = utils.base64_to_text(sc)

    mc = os.getenv("XT_MONGO_CONN_STR")
    mc = utils.base64_to_text(mc)
    #print("init_cred: sc={}, mc={}".format(sc, mc))

    if sc:   # mongo is now optional (tracking mode)
        # XT client on compute node 

        # cleanup (for testing from client)
        sc = sc.replace('\\"', '"')

        # print("sc=", sc)
        sc_data = json.loads(sc)
        store_name = sc_data["name"]
        store_key = utils.safe_value(sc_data, "key")

        sd = {"name": store_name, "key": store_key}

        if mc:
            mc = mc.replace('\\"', '"')
            if mc.startswith('"'):
                mc = mc[1:-1]

            # sample mc: mongodb://xt-sandbox-cosmos:kBOWLQrseZ
            prefix, mc_rest = mc.split("://", 1)
            mc_name, _ = mc_rest.split(":", 1)
            
            md = {"name": mc_name, "key": mc}

    return sd, md

# def get_user_photo(token):
#     import requests
#     import json

#     endpoint =  "https://graph.microsoft.com/v1.0/me/photo/$value"
#     headers = {'Authorization': 'Bearer ' + token}

#     result = requests.get(endpoint, headers=headers)
#     bytes_value = result["content"]

#     return bytes_value


