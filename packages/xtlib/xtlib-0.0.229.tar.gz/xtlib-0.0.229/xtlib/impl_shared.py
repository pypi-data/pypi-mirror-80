#
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT license.
#
# impl_shared.py - code shared between the impl-xxx modules
import os
import shutil
import logging

from xtlib import utils
from xtlib import errors
from xtlib import xt_dict
from xtlib import pc_utils
from xtlib import file_utils

from xtlib.storage.store import Store
from .console import console
from .helpers import xt_config
from xtlib.xt_vault import get_store_and_mongo_creds_on_compute_node

class StoreOnDemand(object):
    '''
    used to delay actual store object for as long as possible
    '''
    def __init__(self, impl_shared):
        self.impl_shared = impl_shared
        self.actual_store = None

    def __getattr__(self, name):
        # someone is requesting access to a property or method of our store wrapper object
        # time to create the real Store
        if not self.actual_store:
            self.actual_store = self.impl_shared.build_actual_store()

        return getattr(self.actual_store, name)

class ImplShared():
    def __init__(self):
        self.config = None
        self.store = StoreOnDemand(self)

    def build_actual_store(self):
        '''
        This defers creating the Store object until is it really needed.  This
        helps with performance on non-store commands and ensures we do all needed
        initialization before creating the Store object.

        NOTE: this function also controls opening the Store using the passed credentials
        (vs. the config file) if we are running on a compute node.
        '''

        console.diag("start of build_actual_store")
        mongo_options = None
        
        # validate USERNAME
        username = self.config.get("general", "username", suppress_warning=True)
        if not username:
            errors.config_error("'username' must be set in the [general] section of XT config file")

        # compute node creds take prioity
        storage_creds, mongo_creds = get_store_and_mongo_creds_on_compute_node()
        if storage_creds:
            # running on COMPUTE NODE
            run_cache_dir = None
            mongo_conn_str = mongo_creds["key"]
            provider_code_path = os.getenv("XT_STORE_CODE_PATH")
            storage_creds["provider"] = provider_code_path.split(".")[2]
            max_log_workers = 0

        else:
            # running on XT CLIENT machine; get them from config files
            storage_creds = self.config.get_storage_creds()
            mongo_creds, mongo_name = self.config.get_mongo_creds()
            run_cache_dir = self.config.get("general", "run-cache-dir")
            provider_code_path = self.config.get_storage_provider_code_path(storage_creds)

            mongo_options = self.config.get("mongo")

            #store_key = storage_creds["key"]
            mongo_conn_str = mongo_creds["mongo-connection-string"]

        self.store = Store(storage_creds, provider_code_path=provider_code_path, run_cache_dir=run_cache_dir, 
            mongo_conn_str=mongo_conn_str, mongo_options=mongo_options)

        console.diag("end of build_actual_store")

        return self.store

    def expand_xt_symbols(self, args):
        for i, arg in enumerate(args):
            
            if "$lastrun" in arg:
                last_run = xt_dict.get_xt_dict_value("last_run", "run0")
                args[i] = arg.replace("$lastrun", last_run)

            if "$lastjob" in arg:
                last_job = xt_dict.get_xt_dict_value("last_job", "job0")
                args[i] = arg.replace("$lastjob", last_job)

            if "$username" in arg:
                username = pc_utils.get_username()
                args[i] = arg.replace("$username", username)

    def init_config(self, fn_local_config, args=None):
        self.config = xt_config.get_merged_config(local_overrides_path=fn_local_config)
        return self.config

    def pre_dispatch_processing(self, dispatch_type, caller, arg_dict):
        # if --job=xxx is specifed, it should overwrite the "ws" property
        # if "job" in arg_dict and "workspace" in arg_dict:
        #     job_id = arg_dict["job"]
        #     ws_id = arg_dict["workspace"]

        #     job_ws = self.store.get_job_workspace(job_id)
        #     if job_ws and job_ws != ws_id:
        #         arg_dict["workspace"] = job_ws
        #         console.diag("specifying job={} has updated workspace to: {}".format(job_id, job_ws))

        if dispatch_type == "command":
            # post process root flags
            if console.level in ["none", "normal"]:
                # turn off all azure warnings
                logging.getLogger("azureml").setLevel(logging.ERROR)


