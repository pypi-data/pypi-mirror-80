import configparser
import os
import stat
from urllib.parse import urlparse


class Config(object):
    def __init__(self):
        self._config = configparser.ConfigParser()
        self._creds = configparser.ConfigParser()
        self._configDir = os.path.expanduser('~') + '/.thus'
        self._configDirExists = os.path.isdir(self._configDir)
        self._configFile = os.path.expanduser('~') + '/.thus/config'
        self._configFileExists = os.path.isfile(self._configFile)
        self._credentialFile = os.path.expanduser('~') + '/.thus/credentials'
        self._credentialFileExists = os.path.isfile(self._credentialFile)

    def ReadExistingConfig(self):
        if self._configFileExists:
            self._config.read(self._configFile)
        if self._credentialFileExists:
            self._creds.read(self._credentialFile)

    def WriteoutConfig(self):
        if not self._configDirExists:
            os.mkdir(path=self._configDir ,mode=0o600)

        if self._configFileExists:
            os.chmod(self._configFile, stat.S_IREAD | stat.S_IWRITE )
        if self._credentialFileExists:
            os.chmod(self._credentialFile, stat.S_IREAD |stat.S_IWRITE )

        with open(self._configFile, mode='w') as configfile:
            self._config.write(configfile)
        with open(self._credentialFile, mode='w') as credsfile:
            self._creds.write(credsfile)

        os.chmod(self._configFile, stat.S_IREAD)
        os.chmod(self._credentialFile, stat.S_IREAD)
        os.chmod(self._configDir, stat.S_IEXEC)

    def _read_input(self, promptText, default=None):
        prompt = promptText.strip()
        if default:
            prompt = prompt + " [ " + default +" ] "
        val = input(prompt).strip()
        if default and (val is None or val == ""):
            val = default
            return val
        while val == "":
            print("A value is required, please enter a value.")
            val = input(prompt).strip()
        return val
    def _verifyHostName(self, host, path=""):
        o = urlparse(host)
        if o.scheme != "https":
            print("Host does not appear to start with https")
            return False
        if o.path != path:
            print("Host does not appear to end with /api")
            return False
        return True

    def ConfigProfileName(self):
        self._profileName = self._read_input(promptText="Enter the profile name to configure", default="default")
        if self._profileName not in self._config:
            self._config[self._profileName] = {}
            self._config_profileExisted = False
        else:
            self._config_profileExisted = True
        if self._profileName not in self._creds:
            self._creds[self._profileName] = {}
            self._creds_profileExisted = False
        else:
            self._creds_profileExisted = True


    def ConfigureDeepSecurity(self):
        deepSecurity = self._read_input(promptText="Do you wish to use Deep Security?", default="yes")
        if deepSecurity.lower() in ['true', '1', 't', 'y', 'ye', 'yes', 'yeah', 'yup', 'certainly']:
            host = self._read_input(promptText="Please enter your Deep Security host, include https:// and end with /api: ")
            while not self._verifyHostName(host=host, path="/api"):
                host = self._read_input(
                    promptText="Please enter your Deep Security host, include https:// and end with /api: ")
            self._config[self._profileName]['DSMhost'] = host
            verifyCert = self._read_input(
                promptText="Do you wish to verify the TLS certificate? Note if your using a self-signed cert, say false here. ",
                default='True')
            if verifyCert.lower() in ['true', '1', 't', 'y', 'yes', 'yeah', 'yup', 'certainly']:
                self._config[self._profileName]['DSMverifyssl'] = 'True'
            else:
                self._config[self._profileName]['DSMverifyssl'] = 'False'

            self._creds[self._profileName]['DSMapikey'] = self._read_input(promptText="Enter your API key")
        return

    def ConfigWorkloadSecurity(self):
        workloadSecurity = self._read_input(promptText="Do you wish to use Cloud One Workload Security?", default="yes")
        if workloadSecurity.lower() in ['true', '1', 't', 'y','ye', 'yes', 'yeah', 'yup', 'certainly']:
            self._config[self._profileName]['DSMverifyssl'] = 'True'
            self._config[self._profileName]['DSMhost'] = 'https://app.deepsecurity.trendmicro.com/api'
            self._creds[self._profileName]['DSMapikey'] = self._read_input(promptText="Enter your API key")
            return True
        return False

    def ConfigSmartCheck(self):
        smartcheck = self._read_input(promptText="Do you wish to use SmartCheck?", default="no")
        if smartcheck.lower() in ['true', '1', 't', 'y', 'ye', 'yes', 'yeah', 'yup', 'certainly']:
            host = self._read_input(
                promptText="Please enter your Smart Check host, include https:// and do not include /api: ")
            while not self._verifyHostName(host=host, path=""):
                host = self._read_input(
                    promptText="Please enter your Smart Check host, include https:// and do not include /api: ")
            self._config[self._profileName]['SChost'] = host
            verifyCert = self._read_input(
                promptText="Do you wish to verify the TLS certificate? Note if your using a self-signed cert, say false here. ",
                default='False')
            if verifyCert.lower() in ['true', '1', 't', 'y', 'yes', 'yeah', 'yup', 'certainly']:
                self._config[self._profileName]['SCverifyssl'] = 'True'
            else:
                self._config[self._profileName]['SCverifyssl'] = 'False'

            self._creds[self._profileName]['SCUser'] = self._read_input(promptText="Enter your Smart Check user name")
            self._creds[self._profileName]['SCPassword'] = self._read_input(promptText="Enter your Smart Check password")

        return

    def ConfigCloudConformity(self):
        CloudConformity = self._read_input(promptText="Do you wish to use Cloud Conformity?", default="no")
        if CloudConformity.lower() in ['true', '1', 't', 'y', 'ye', 'yes', 'yeah', 'yup', 'certainly']:
            host = ""
            while host == "":
                region = self._read_input(
                    promptText="Please enter your endpoint region (eu-west-1 or ap-southeast-2 or us-west-2):", default="us-west-2")
                if region.strip().lower() == 'us-west-2':
                    host = 'https://us-west-2-api.cloudconformity.com/v1'
                elif region.strip().lower() == 'ap-southeast-2':
                    host = 'https://ap-southeast-2-api.cloudconformity.com/v1'
                elif region.strip().lower() == 'eu-west-1':
                    host = 'https://eu-west-1-api.cloudconformity.com/v1'
                else:
                    print("Please select from one of the available zones.")
            self._config[self._profileName]['CCendpoint'] = host
            self._creds[self._profileName]['CCapikey'] = self._read_input(promptText="Enter your API key")

    def RunConfig(self):
        self.ReadExistingConfig()
        self.ConfigProfileName()
        if not self.ConfigWorkloadSecurity():
            self.ConfigureDeepSecurity()
        self.ConfigSmartCheck()
        self.ConfigCloudConformity()
        self.WriteoutConfig()
