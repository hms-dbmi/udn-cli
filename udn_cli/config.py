import os
import configparser


class Config:
    def __init__(self, args):
        # read in user's config (defaults to ~/.udn/config)
        config = configparser.ConfigParser()
        default_config_path = os.path.expanduser('~/.udn/config')
        config_path = os.getenv('UDN_CONFIG', default_config_path)
        config.read(config_path)

        section = 'PROD'
        if args.test:
            section = 'TEST'

        self.host = config[section]['host']
        self.udn_token = config[section]['udn_token']
        self.fileservice_token = config[section]['fileservice_token']
        self.bucket = config[section]['bucket']


class SingleUploadConfig(Config):
    def __init__(self, args):
        super(SingleUploadConfig, self).__init__(args)

        # read in positional args
        self.file_path = args.file_path
        self.file_name = os.path.split(args.file_path)[-1]
        self.patient_uuid = args.patient_uuid
        self.seq_request_id = args.seq_request_id

        # read in optional args
        self.metadata = {}
        if args.metadata:
            self.metadata = args.metadata


class MultiUploadConfig(Config):
    def __init__(self, args):
        super(MultiUploadConfig, self).__init__(args)

        # read in positional args
        self.directory = args.directory
