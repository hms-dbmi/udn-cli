import os
import json
import configparser


class Config:
    def __init__(self, args):
        # read in user's config (defaults to ~/.udn/config)
        config = configparser.ConfigParser()
        default_config_path = os.path.expanduser('~/.udn/config')
        config_path = os.getenv('UDN_CONFIG', default_config_path)
        config.read(config_path)

        section = 'PROD'
        self.permissions = ['udn']
        if args.test:
            section = 'TEST'
            self.permissions = ['udntest']

        self.host = config[section]['host']
        self.udn_token = config[section]['udn_token']
        self.fileservice_token = config[section]['fileservice_token']
        self.bucket = config[section]['bucket']


class SingleUploadConfig(Config):
    def __init__(self, args):
        super().__init__(args)

        # read in positional args
        self.file_path = args.file_path
        self.file_name = os.path.split(args.file_path)[-1]

        # read in optional args
        self.force = args.force
        self.metadata = {}

        if args.metadata:
            self.metadata = json.loads(args.metadata)

        if args.bucket:
            self.bucket = args.bucket


class MultiUploadConfig(Config):
    def __init__(self, args):
        super().__init__(args)

        # read in positional args
        self.directory = args.directory

        # read in optional args
        self.force = args.force
