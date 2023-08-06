import copy
import os
import json
import ntpath
import shutil
import warnings
import logging
# logging.basicConfig(level=logging.DEBUG)
from abc import ABC
from pathlib import Path

import jwt

import d6tcollect

from d6tpipe.http_client import client as python_http_client
from d6tpipe.utils.utils import ClientTiny, loadjson, _dict_sort

class ConfigManager(object):

    """

    Manage local config. The config is stored in JSON and can be edited directly `filecfg` location, by default '~/d6tpipe/cfg.json'

    Args:
        profile (str): name of profile to use
        filecfg (str): path to where config file is stored 

    """

    def __init__(self, profile=None, filecfg='~/d6tpipe/cfg.json'):
        self.profile = 'default' if profile is None else profile
        if str(filecfg).startswith('~'):
            filecfg = os.path.expanduser(filecfg)
        self.filecfg = filecfg

    def init(self, config=None, server='https://pipe.databolt.tech', reset=False):
        """

        Initialize config with content

        Args:
            config (dict): manually pass config object
            server (str): location of REST API server
            reset (bool): force reset of an existing config

        """

        if os.path.exists(self.filecfg) and not reset and self.profile in self._loadall():
            # todo: why does Path(self.filecfg).exists() not work in pytest?
            warnings.warn('Config for profile {} in {} already exists, skipping init. Use reset=True to reset config.'.format(self.profile,self.filecfg))
            return None

        if not config:
            config = {}
        if 'server' not in config:
                config['server'] = server
        if 'filerepo' not in config:
            config['filerepo'] = '~/d6tpipe'
        p = Path(config['filerepo'])
        p2 = p/'files/{}/'.format(self.profile)
        config['filereporoot'] = str(p)
        config['filerepo'] = str(p2)
        if 'filedb' not in config:
            config['filedb'] = str(p2/'.filedb.json')

        # create config file if doesn't exist
        if not os.path.exists(self.filecfg):
            if not os.path.exists(ntpath.dirname(self.filecfg)):
                os.makedirs(ntpath.dirname(self.filecfg))

        self._save(config)

    def update(self, config):
        """

        Update config. Only keys present in the new dict will be updated, other parts of the config will be kept as is. In other words you can pass in a partial dict to update just the parts you need to be updated.

        Args:
            config (dict): updated config

        """

        configall = self._loadall()
        config_current = configall[self.profile]
        config_current.update(config)
        self._save(config_current)
        return True

    def _save(self, config):
        if os.path.exists(self.filecfg):
            configall = self._loadall()
            configall[self.profile] = config
        else:
            configall = {}
        configall[self.profile] = config
        with open(self.filecfg, 'w') as f:
            json.dump(configall, f, indent=4)
        return True

    def _loadall(self):
        if not os.path.exists(self.filecfg):
            self.init()
            print('auto created profile "{}", see docs how to customize profile'.format(self.profile))
        with open(self.filecfg, 'r') as f:
            config = json.load(f)
        return config

    def load(self):
        """

        Loads config

        Returns:
            dict: config

        """

        config = self._loadall()
        if self.profile not in config:
            self.init()
            config = self._loadall()
            warnings.warn('auto created profile "{}", see docs how to customize profile'.format(self.profile))
        config = config[self.profile]
        for ikey in ['filereporoot','filerepo','filedb']:
            if config[ikey].startswith('~'):  # do this dynamically
                config[ikey] = os.path.expanduser(config[ikey])
        if not os.path.exists(config['filerepo']):
            os.makedirs(config['filerepo'])

        return config


class _APIBase(metaclass=d6tcollect.Collect):

    def __init__(self, config=None, profile=None, filecfg='~/d6tpipe/cfg.json'):
        self.profile = 'default' if profile is None else profile
        if config is None:
            self.configmgr = ConfigManager(filecfg=filecfg, profile=self.profile)
            self.config = self.configmgr.load()
        else:
            self.config = config
            warnings.warn("Using manual config override, some api functions might not work")

        self.cfg_profile = self.config
        self.cfg_filecfg = filecfg
        self.filerepo = self.cfg_profile['filerepo']
        self.dir = self.filerepo
        self.dirpath = Path(self.dir)

        self.key = self.cfg_profile.get('key',None)
        if self.key is None:
            # print("Auto generated an encryption key, update the config if you want to use your own")
            import uuid
            self.key = str(uuid.uuid4())
            self.configmgr.update({'key':self.key})

        self.encrypt_keys = ['location','readCredentials','writeCredentials','settings','files','readParams']

    def list_pipes(self, names_only=True, parent_only=False):
        """

        List all pipes you have access to

        Args:
            names_only (bool): if false, return all details

        """
        r = self.cnxn.pipes.get()[1]
        if parent_only:
            r = [o for o in r if not o.get('parent')]
        if names_only:
            r = sorted([o['name'] for o in r])
        return r

    def wipe_all(self, confirm=True):
        """

        Remove all d6tpipe files. WARNING: this can't be undone

        Args:
            confirm (bool): ask for user confirmation

        """

        if confirm:
            c = input('Confirm deleting files in {}. WARNING: this cannot be undone (y/n)'.format(self.dir))
        else:
            c = 'y'
        if c=='y':
            del self.cnxn
            shutil.rmtree(self.filerepo)
            os.remove(self.configmgr.filecfg)

    def list_local_pipes(self):
        """

        List all pipes already pulled

        Returns:
            list: list of pipe names

        """
        dirs = [ name for name in os.listdir(self.filerepo) if os.path.isdir(os.path.join(self.filerepo, name)) ]
        return [name for name in dirs if os.listdir(os.path.join(self.filerepo, name))]

    def move_repo(self, path):
        """

        Moves all files to another location and updates the config

        Args:
            path (pathlib.Path):

        Returns:
            bool:

        """

        Path(path).mkdir(parents=True, exist_ok=True)
        shutil.move(self.filerepo,path)
        self.configmgr.update({'filerepo': path})
        print('Moved repo to {}. Reloading api'.format(path))
        self.__init__(profile=self.profile, filecfg=self.cfg_filecfg)

        return True

    def encode(self, dict_):
        """

        Encrypt

        Args:
            dict_ (dict):

        Returns:
            dict: all values encrypted, keys are kept as is

        """

        raise NotImplementedError('Sign up for premium features to access this function, email support@databolt.tech')

    def decode(self, dict_):
        """

        Decrypt

        Args:
            dict_ (dict):

        Returns:
            dict:

        """

        raise NotImplementedError('Sign up for premium features to access this function, email support@databolt.tech')

class APILocal(_APIBase,metaclass=d6tcollect.Collect):

    """

    As an alternative to the remote API, you can store everything locally. It mirrors the basic funtionality of the remote API but is not as feature rich.

    Args:
        config (dict): manually pass config object
        profile (str): name of profile to use
        filecfg (str): path to where config file is stored 

    """

    def __init__(self, config=None, profile=None, filecfg='~/d6tpipe/cfg.json'):
        super().__init__(config,profile,filecfg)
        self.cnxn = ClientTiny(self.config['filedb'])
        self.mode = 'local'


class APIClient(_APIBase, metaclass=d6tcollect.Collect):

    """

    Manager to interface with the remote API. 

    Args:
        token (str): your API token
        config (dict): manually pass config object
        profile (str): name of profile to use
        filecfg (str): path to where config file is stored 

    """

    def __init__(self, token='config', config=None, profile=None, filecfg='~/d6tpipe/cfg.json'):
        super().__init__(config,profile,filecfg)
        if token=='config':
            self.token = self.cfg_profile.get('token',None)
        else:
            self.token = token
        if self.token is not None:
            request_headers = {
                "Authorization": 'Token {0}'.format(self.token)
            }
        else: # if not registered
            request_headers = {}
        client = python_http_client.Client(host=self.cfg_profile['server'],
                                           request_headers=request_headers,
                                           append_slash=True,
                                           version='1')
        self.cnxn = client.api
        self.mode = self.cfg_profile.get('mode','local')

        if self.token is not None:
            # test connection
            try:
                r,d = self.cnxn.get()
                if 'databolt.tech' in self.cfg_profile['server'] and 'username' not in d:
                    warnings.warn('API authentication error')
                else:
                    self.username = d.get('username')
                    print('Connected to {} as {}'.format(self.cfg_profile['server'],self.username))
                    if 'message' in d:
                        print(d['message'])
            except Exception as e:
                warnings.warn('API connection error ' + str(e))
        else:
            print('No token provided. Register or login to connect to repo API.')

    def register(self, username, email, password):
        """

        Register a new API user

        Args:
            username (str): 
            email (str): 
            password (str): 

        """

        data = {'username': username, 'email': email, 'password': password}
        # response, data = self.cnxn.accounts.post(request_body=data)
        try:
            response, data = self.cnxn.accounts.post(request_body=data)
        except Exception as e:
            if 'This field must be unique' in str(e):
                warnings.warn("Username or email already registered, registration failed. Pick a different username if you haven't registered before. If you already registered and forgot your token, call api.forgotToken(). If you want to re-register provide a different username")
                return
            else:
                raise e
        token = data.get('token')
        self._printtoken(token)
        return token

    def login(self, username, password):
        """

        Login if already registered

        Args:
            username (str): 
            password (str): 

        """

        return self.forgotToken(username, password)

    def forgotToken(self, username, password):
        """

        Retrieve your API token

        Args:
            username (str): 
            password (str): 

        """

        data = {'username': username, 'password': password}
        response, data = self.cnxn.accounts.token.post(request_body=data)
        token = data.get('token')
        self._printtoken(token)
        return token

    def setToken(self, token):
        self._printtoken(token)

    def _printtoken(self, token):
        print('Your token is below. Please save it and KEEP IT SAFE! If you forget it, you can retrieve it with APIClient().forgotToken(username, password)')
        print(token)
        print('reloading api to update token')
        self.configmgr.update({'token': token})
        self.__init__(profile=self.profile, filecfg=self.cfg_filecfg)

    def _unregister(self, username):
        self.cnxn.accounts._(username).delete()
        self.configmgr.update({'token': None})


@d6tcollect.collect
def list_profiles(filecfg='~/d6tpipe/cfg.json'):
    if str(filecfg).startswith('~'):
        filecfg = os.path.expanduser(filecfg)
    print(open(filecfg).read())

@d6tcollect.collect
def upsert_resource(apiroot, settings):

    """

    Convenience function to create or update a resource

    Args:
        apiroot (obj): API endpoint root eg `api.cnxn.pipes`
        settings (dict): resource settings

    Returns:
        response (obj): server response
        data (dict): json returned by server

    """

    try:
        r, d = apiroot._(settings['name']).patch(request_body=settings)
    except Exception as e:
        if 'Not found' in str(e):
            return apiroot.post(request_body=settings)
        else:
            raise e
    return apiroot._(settings['name']).get()

@d6tcollect.collect
def upsert_pipe(api, settings):

    """

    Convenience function to create or update a pipe

    Args:
        api (obj): api
        settings (dict): pipe settings

    Returns:
        response (obj): server response
        data (dict): json returned by server

    """

    return upsert_resource(api.cnxn.pipes, settings)

@d6tcollect.collect
def upsert_permissions(api, pipe_name, settings):

    """

    Convenience function to create or update pipe permissions

    Args:
        api (obj): api
        settings (dict): permission settings

    Returns:
        response (obj): server response
        data (dict): json returned by server

    """

    apiroot = api.cnxn.pipes._(pipe_name).permissions
    # for now just post to permissions
    return apiroot.post(request_body=settings)

def upsert_pipe_json(api, path_json, name):

    """

    Convenience function to create or update a resource. Loads settings from config file to secure credentials

    Args:
        api (obj): api
        path_json (str): path to config file in json format
        name (str): name of json entry

    Returns:
        response (obj): server response
        data (dict): json returned by server

    """

    settings = loadjson(path_json)[name]
    return upsert_pipe(api, settings)
