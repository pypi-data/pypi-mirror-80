#  Copyright (c) 2020. Brendan Johnson. All Rights Reserved.

import sys
import signal
import json
import DeepSecurity
import SmartCheck
import CloudConformity
import argparse
from inspect import getmembers, isfunction, signature

import logging

from .session import Session
from .config import Config
LOG = logging.getLogger('thus.clidriver')
LOG_FORMAT = (
    '%(asctime)s - %(threadName)s - %(name)s - %(levelname)s - %(message)s')
executablePath = ""
# Don't remove this line.  The idna encoding
# is used by getaddrinfo when dealing with unicode hostnames,
# and in some cases, there appears to be a race condition
# where threads will get a LookupError on getaddrinfo() saying
# that the encoding doesn't exist.  Using the idna encoding before
# running any CLI code (and any threads it may create) ensures that
# the encodings.idna is imported and registered in the codecs registry,
# which will stop the LookupErrors from happening.
# See: https://bugs.python.org/issue29288
u''.encode('idna')

def _set_user_agent_for_session(session):
    session.user_agent_name = 'thus-cli'
 #   session.user_agent_version = __init__.__version__


def main(exePath):
    executablePath = exePath
    driver = create_clidriver()
    rc = driver.main()
    return rc

def create_clidriver():
    session =  Session()
    _set_user_agent_for_session(session)
    #load_plugins(session.full_config.get('plugins', {}),
    #             event_hooks=session.get_component('event_emitter'))
    driver = CLIDriver(session=session)
    return driver

def setCLIParse():
    parser = argparse.ArgumentParser(description='THUS CLI' )
    # Add the arguments
    parser.add_argument('--config',
                           action='store_true',
                           help='Run configuration')
    parser.add_argument('--verbose','-v',
                           action='store_true',
                           help='Turn on verbose mode')
    parser.add_argument('--profile',
                        action='store',
                        default='default',
                        help='Profile name to use')
    parser.add_argument('service',
                        action='store',
                        nargs='?',
                        help='The service you which to address.')
    parser.add_argument('module',
                        action='store',
                        nargs='?',
                        help='The the module within the service you which to address.')
    parser.add_argument('function',
                        action='store',
                        nargs='?',
                        help='The function in the module within the service you which to address.')
    parser.add_argument('function_arguments',
                        action='store',
                        nargs='*')
    t = parser.parse_known_args()

    return t


class CLIDriver(object):

    def __init__(self, session=None):
        #self._functions_list = [o for o in getmembers(deepsecurity) if isfunction(o[1])]
        self._functions = dir(DeepSecurity)
        if session is None:
            self.session = Session()
        else:
            self.session = session
        self._args = setCLIParse()
        self._profile = self._args[0].profile
       # self.alias_loader = AliasLoader()

    def parseCliFlag(self, arg):
        split = arg.split("=")
        if(split[0] == "--profile"):
            self._profile = split[1]

    def parseCommand(self):
        if self._args[0].config:
            ConfObj = Config()
            ConfObj.RunConfig(exePath=executablePath)
            sys.exit()
        self._service = self._args[0].service
        self._command = self._args[0].module
        self._subcommand = self._args[0].function
        self._arguments = {}

        if len(self._args[0].function_arguments) > 0:
            for s in self._args[0].function_arguments:
                split=s.split("=")
                if split[0] == 'payload':
                    self._arguments[split[0]] = json.loads(split[1])
                else:
                    self._arguments[split[0]]=split[1]



    def FindClass(self, module):
        listing = dir (module)
        for c in listing:
            if c.lower() == self._command.lower():
                self._command = c
                break
        classToCall = getattr(module, self._command)
        return classToCall
    def FindFunction(self, rtv):
        listing = dir(rtv)
        for f in listing:
            if f.lower() == self._subcommand.lower():
                self._subcommand = f
                break
        method_to_call = getattr(rtv, self._subcommand)
        return method_to_call

    def ExecuteCommand(self):
        service = self._service.lower()
        if service == 'cc' or service == 'cloudconformity':
            config = self.session.BuildCCConfig(profile=self._profile)
            connection = CloudConformity.connect.Connection(config=config)
            group_to_call = self.FindClass(module=CloudConformity)
            rtv = group_to_call(config=config, connection=connection)
            method_to_call = self.FindFunction(rtv=rtv)
            rtv = method_to_call(*self._arguments)
        if service == 'workloadsecurity' or service == 'ws':
            #Place holder until WS diverges from DS
            service = 'deepsecurity'
        if service == 'containersecurity' or service == 'cs':
            # Place holder until sc diverges rom cs
            service = 'smartcheck'
        if service == 'deepsecurity' or service=='ds':
            config = self.session.BuildDSMConfig(profile=self._profile)
            connection = DeepSecurity.connect.Connection(config=config)
            group_to_call = self.FindClass(module=DeepSecurity)
            rtv = group_to_call(config=config, connection=connection)
            method_to_call = self.FindFunction(rtv=rtv)
            rtv = method_to_call(**self._arguments)
        if service == 'smartcheck' or service == 'sc':
            config = self.session.BuildSCConfig(profile=self._profile)
            connection = SmartCheck.connect.Connection(config=config)
            group_to_call = self.FindClass(module=SmartCheck)
            rtv = group_to_call(config=config, connection=connection)
            method_to_call = self.FindFunction(rtv=rtv)
            rtv = method_to_call(*self._arguments)
        return rtv

    def printResults(self, results):
        try:
            print(json.dumps(results))
        except:
            print(results)

    def main(self):
        self.parseCommand()
        results = self.ExecuteCommand()
        self.printResults(results)